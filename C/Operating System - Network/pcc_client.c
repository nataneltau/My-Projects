#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
#include <errno.h>
#include <endian.h>

/* credits
 * implementation of client and server: code from exercise 10 && https://www.youtube.com/watch?v=io2G2yW1Qk8 
 * && https://idiotdeveloper.com/file-transfer-using-tcp-socket-in-c/
 * help with files: https://stackoverflow.com/questions/238603/how-can-i-get-a-files-size-in-c && 
 * https://stackoverflow.com/questions/16095248/convert-long-long-to-string-in-c
 * 
*/



int main(int argc, char *argv[]){

    if(argc != 4){
        fprintf( stderr, "%s\n", strerror(errno));
        exit(1);
    }

    int  sockfd     = -1;
    uint64_t file_size = 0;
    int  bytes_read =  0;
    char recv_buff[1024];
    int temp;
    FILE *file_read;
    char *ip = argv[1];
    char *fsize_char;
    //char fsize[100];
    uint16_t porti = atoi(argv[2]);
    uint64_t fsize, pri;
    int nsent, total_sent, num_of_read;
    //char mb_buff[1024*1024];


    

    struct sockaddr_in addr; // where we Want to get to
    //socklen_t addrsize = sizeof(struct sockaddr_in );



    file_read = fopen(argv[3], "r");

    if(file_read == NULL){//error in open file
        fprintf( stderr, "%s\n", strerror(errno));
        exit(1);
    }

    memset(recv_buff, 0,sizeof(recv_buff));

    
    if( (sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0){
        fprintf( stderr, "%s\n", strerror(errno));
        exit(1);
    }

    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(porti); // Note: htons for endiannes
    addr.sin_addr.s_addr = inet_addr(ip); // at test need to use 127.0.0.1



    // connect socket to the target address
    if( connect(sockfd, (struct sockaddr*) &addr, sizeof(addr)) < 0){
        fprintf( stderr, "%s\n", strerror(errno));
        exit(1);
    }

    //this section check for the file size and then send it to the server
    fseek(file_read, 0, SEEK_END);
    file_size = ftell(file_read);
    rewind(file_read);
    //printf("file size is: %lu\n", file_size);
    /*sprintf(fsize, "%ld", file_size);
    strcpy(recv_buff, fsize);
    temp = write(sockfd, recv_buff, strlen(recv_buff));*/

    // write file size to server
	fsize = (htobe64(file_size));
	fsize_char = (char*)&fsize;
	total_sent = 0;
	while(total_sent < 8){//should be 8 bytes
		temp = write(sockfd, fsize_char+total_sent, 8-total_sent);
		if(temp < 0){
			fprintf( stderr, "%s\n", strerror(errno));
            exit(1);
		}
		total_sent += temp;
	}

    memset(recv_buff, 0,sizeof(recv_buff));
    /*memset(recv_buff, 0,sizeof(recv_buff));
    temp = read(sockfd, recv_buff, sizeof(recv_buff));

    if(strcmp("got", recv_buff)){
        printf("something went wrong\n");//for debug
    }*/

	
	//printf("we start writing\n");
    
    //write data to the server
    while(fread(recv_buff, 1, 1024, file_read) != 0){

        temp = strlen(recv_buff);
        total_sent = 0;

        if(temp < 1024){
            num_of_read = temp;
        }
        else{
            num_of_read = 1024;
        }
        
        //printf("we read line and num of read is: %d\n", num_of_read);

        while(total_sent<1024){
        
        	//printf("we writing\n");

            nsent = write(sockfd, recv_buff+total_sent, 1024- total_sent);
        
            if(nsent<0){// check if error occured (server closed connection?)
                fprintf( stderr, "%s\n", strerror(errno));
                exit(1);
            }

            total_sent += nsent;
            
            //printf("total_sent is: %d\n", total_sent);

        }//end of inner while
        
        //printf("we are out of inner while\n");

        memset(recv_buff, 0,sizeof(recv_buff));

    }//end of while
    
    //printf("we are out of while, start reading\n");

    bytes_read = 0;

    while(bytes_read < 8){
        temp = read(sockfd, fsize_char+bytes_read, 8-bytes_read);

        if(temp<0){// check if error occured (server closed connection?)
            fprintf( stderr, "%s\n", strerror(errno));
            exit(1);
        }

        bytes_read += temp;

    }

    // read data from server into recv_buff
    // block until there's something to read
    // print data to screen every time
    
    //bytes_read = read(sockfd, recv_buff, sizeof(recv_buff) - 1);
    //recv_buff[bytes_read] = '\0';
    
    pri = be64toh(fsize);

    printf("# of printable characters: %lu\n", pri);

    close(sockfd);

    if(temp>0 || num_of_read>0){//for compile
        temp++;
    }

    return 0;



}//end of function main
