import contextlib
import os
import numbers

from q2_atm import ATM, ServerResponse
from infosec import core


def decrypt_with(module_path, function_name, what, encrypted_value, expected_type):
    with core.smoke.get_from_module(module_path, function_name) as function:
        try:
            decrypted_value = function(encrypted_value)
        except Exception as e:
            raise core.SmoketestFailure(
                f'Exception decrypting {what} using {module_path}') from e
    core.smoke.type_check(decrypted_value, expected_type,
                           f'Invalid type for decrypted {what} using {module_path}')
    return decrypted_value


def check_extraction(module_path, function_name, what, value, encryption_func, expected_type):
    encrypted_val = encryption_func(value)
    decrypted_val = decrypt_with(
        module_path, function_name, what, encrypted_val, expected_type)
    if decrypted_val != value:
        raise core.SmoketestFailure(
            f'Decryption of {what} doesn\'t work for {repr(value)} - result was {repr(decrypted_val)}')
    core.smoke.success(f'Decryption of {what} succeeded for a sample input')


@contextlib.contextmanager
def get_cipher(module_path, key):
    with core.smoke.get_from_module(module_path, 'RepeatedKeyCipher') as cipher_class:
        yield cipher_class(key)


@contextlib.contextmanager
def get_breaker(module_path):
    with core.smoke.get_from_module(module_path, 'BreakerAssistant') as breaker_class:
        yield breaker_class()


def check_q1a(module_path):
    with get_cipher(module_path, b'abc') as cipher:
        try:
            encrypted = cipher.encrypt('abcab')
        except Exception as e:
            raise core.SmoketestFailure(
                f'Exception encrypting with {module_path}') from e

    if not isinstance(encrypted, bytes):
        raise core.SmoketestFailure(
            f"Encryption with {module_path} doesn't return `bytes`, it returns a {type(encrypted)}")

    if encrypted != bytes([0] * 5):
        raise core.SmoketestFailure(
            f'Encryption doesnt seem right with {module_path}')

    core.smoke.success(f'Result looks like an encrypted value')


def check_q1b(module_path):
    with get_cipher(module_path, b'abc') as cipher:
        try:
            decrypted = cipher.decrypt(b')+CUP')
        except Exception as e:
            raise core.SmoketestFailure(
                f'Exception decrypting with {module_path}') from e

    if not isinstance(decrypted, str):
        raise core.SmoketestFailure(
            f"Decryption with {module_path} doesn't return `str`, it returns a {type(decrypted)}")

    if decrypted != 'HI 42':
        raise core.SmoketestFailure(
            f'Decryption doesnt seem right with {module_path}')

    core.smoke.success(f'Decryption succeeded for a known test value')


def check_q1c(module_path):
    def breaker_score(breaker, text):
        try:
            result = breaker.plaintext_score(text)
        except Exception as e:
            raise core.SmoketestFailure(
                f'Error computing plaintext scores with {module_path} on {repr(text)}') from e
        if not isinstance(result, numbers.Number):
            raise core.SmoketestFailure(
                f'Generated score by {module_path} for {repr(text)} is {repr(result)} (not a number!)')
        return result

    with get_breaker(module_path) as breaker:
        text1 = '1A\xfe~\xf6'
        text2 = 'Hello'
        if breaker_score(breaker, text1) >= breaker_score(breaker, text2):
            core.smoke.warning(f'The score of {repr(text1)} is higher than the score of {repr(text2)}. While'
                                'not strictly an error, this is probably bad')
        else:
            core.smoke.success(f'Score seems reasonable for some sample inputs')



def check_q1d(module_path):
    with get_breaker(module_path) as breaker:
        try:
            result = breaker.brute_force(b'\x01\x02\x03\x04\x05', 2)
        except Exception as e:
            raise core.SmoketestFailure(
                f'Error brute forcing cipher text with {module_path}') from e
    if not isinstance(result, str):
        raise core.SmoketestFailure(
            f"Brute forcing with {module_path} doesn\'t return a string, it returns a {type(result)}")


def check_q1e(module_path):
    with get_breaker(module_path) as breaker:
        try:
            print('Testing a long input with a long key. This should complete in under 20 seconds.')
            result = core.smoke.timed_run(
                num_secs=20,
                action=lambda: breaker.smarter_break(b'a' * 32, 16),
                timeout_message=f'Smart break with {module_path} timed out (20 seconds)'
            )
        except TimeoutError:
            raise core.SmoketestFailure(
                f'Smart break with {module_path} timed out (10 seconds)')
        except Exception as e:
            raise core.SmoketestFailure(
                f'Error smart breaking with {module_path}') from e

    if not isinstance(result, str):
        raise core.SmoketestFailure(
            f"Smart breaking with {module_path} doesn\'t return a string, it returns a {type(result)}")

    core.smoke.success("Decryption isn't stuck for a sample long key (we did not check the decrypted value)")

def check_q2a(module_path):
    check_extraction(
        module_path=module_path,
        function_name='extract_PIN',
        what='PIN', value=1234,
        encryption_func=ATM().encrypt_PIN,
        expected_type=int
    )


def check_q2b(module_path):
    check_extraction(
        module_path=module_path,
        function_name='extract_credit_card',
        what='credit card', value=123456789,
        encryption_func=ATM().encrypt_credit_card,
        expected_type=int
    )


def check_q2c(module_path):
    with core.smoke.get_from_module(module_path, 'forge_signature') as forge_signature:
        try:
            signature = forge_signature()
        except Exception as e:
            raise core.SmoketestFailure(
                f'Exception forging a signature with {module_path}') from e

    if not isinstance(signature, ServerResponse):
        raise core.SmoketestFailure(
            f'Signature should be a ServerResponse but is a {type(signature)}')

    try:
        if not ATM().verify_server_approval(signature):
            raise core.SmoketestFailure(
                f'Verification does not pass with signature from {module_path}')
    except Exception as e:
        raise core.SmoketestFailure(
            f'Exception while running the verification on response from {module_path}') from e

    core.smoke.success('Forged signature passedd the server approval')


@contextlib.contextmanager
def question_context(name):
    try:
        core.smoke.highlight(name)
        yield
    except Exception as e:
        core.smoke.error(e)
    finally:
        # Add a new-line after each question
        print()


def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with question_context('Questions 1A'):
        check_q1a('q1.py')

    with question_context('Questions 1B'):
        check_q1b('q1.py')

    with question_context('Questions 1C'):
        check_q1c('q1.py')
        core.smoke.check_if_nonempty('q1c.txt')

    with question_context('Questions 1D'):
        check_q1d('q1.py')
        core.smoke.check_if_nonempty('q1d.txt')

    with question_context('Questions 1E'):
        check_q1e('q1.py')
        core.smoke.check_if_nonempty('q1e.txt')

    with question_context('Questions 2A'):
        check_q2a('q2.py')
        core.smoke.check_if_nonempty('q2a.txt')

    with question_context('Questions 2B'):
        check_q2b('q2.py')
        core.smoke.check_if_nonempty('q2b.txt')

    with question_context('Questions 2C'):
        check_q2c('q2.py')
        core.smoke.check_if_nonempty('q2c.txt')


if __name__ == '__main__':
    smoketest()
