#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <time.h>
#include <signal.h>

#define shifting 32

typedef struct pcc_total{

    uint64_t counter_of_use;
    char printable;

}pcc_total;

pcc_total counter_arr[95];
uint64_t the_updator[95];

int was_signal = 0;
int client_socket = -1;
int we_work = -1;


void init_pcc(){


    for(int i = 0; i<95; i++){
        counter_arr[i].printable = i+shifting;
        counter_arr[i].counter_of_use = 0;
    }

}//end of function init_pcc

int is_printable_and_update(char c){

    if(32<=c && c<=126){
        //counter_arr[c-shifting].counter_of_use++;
        return 1;
    }

    return 0;

}//end of function is_printable

void print_res(){

    for(int i = 0; i<95; i++){
        counter_arr[i].printable = i+shifting;
        //counter_arr[i].counter_of_use = 0;
    }

    for(int i = 0; i<95; i++){

        printf("char '%c' : %lu times\n", counter_arr[i].printable, counter_arr[i].counter_of_use);

    }
}

void mySignalHandler(int signum) {
    if(client_socket <0 && we_work <0){//there is no clinet
        print_res();
        exit(0);
    }

    was_signal = 1;//will exit after finish with client

}

int main(int argc, char *argv[]){

    if(argc != 2){
        fprintf( stderr, "%s\n", strerror(errno));
        exit(1);
    }

    //int totalsent = -1;
    int nsent     = -1;
    int total_printable;
    int temp = 1;
    int server_sock  = -1;
    //int client_socket    = -1;
    uint64_t total_read = 0;
    uint16_t porti = atoi(argv[1]);
    uint64_t fsize = 0;
    char *for_fsize;
    //char ret_printable[100];

    struct sockaddr_in serv_addr;
    socklen_t addrsize = sizeof(struct sockaddr_in );

    char data_buff[1024];

    //init_pcc();//if main if called every time connection has been made, it's a problem

    struct sigaction newAction = {.sa_handler = mySignalHandler};
    // Overwrite default behavior for ctrl+c
    if (sigaction(SIGINT, &newAction, NULL) == -1) {
        perror("Signal handle registration failed");
        exit(1);
    }

    server_sock = socket( AF_INET, SOCK_STREAM, 0 );
    if(server_sock < 0){
        fprintf( stderr, "%s\n", strerror(errno));
        exit(1);
    }

    if(setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, &temp, sizeof(int)) < 0){
        fprintf( stderr, "%s\n", strerror(errno));
        exit(1);
    }

    memset( &serv_addr, 0, addrsize );

    serv_addr.sin_family = AF_INET;
    // INADDR_ANY = any local machine address
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(porti);

    if( 0 != bind( server_sock, (struct sockaddr*) &serv_addr, addrsize)){
        fprintf( stderr, "%s\n", strerror(errno));
        exit(1);
    }

    if( 0 != listen( server_sock, 10 ) ){
        fprintf( stderr, "%s\n", strerror(errno));
        exit(1);
    }



    while( 1 ){
        // Accept a connection. Can use NULL in 2nd and 3rd arguments 
        //if we dont want to print the client socket details
        if(was_signal){//there was SIGINT sometime, now we will exit
            break;
        }
        
        //printf("we wait\n");

        for(int j=0; j<95; j++){
            the_updator[j] = 0;
        }

        client_socket = accept( server_sock, NULL, NULL);

        if( client_socket < 0 ){//accept failed
            fprintf( stderr, "%s\n", strerror(errno));
            exit(1);
        }
        
        //printf("we accept\n");

        we_work = 1;

        memset(data_buff, 0,sizeof(data_buff));
        //temp = read(client_socket, data_buff, sizeof(data_buff));
        //fsize = strtol(data_buff, NULL, strlen(data_buff));

        for_fsize = (char*)&fsize;
        total_read = 0;
        temp = 1;
        while (temp > 0){

            temp = read(client_socket, for_fsize+total_read, 8-total_read);
		    if(temp < 0){
			    break;
		    }
		    total_read += temp;

	    }

	    if(temp < 0 ){
            if (errno == ETIMEDOUT || errno == ECONNRESET || errno == EPIPE){
                fprintf( stderr, "%s\n", strerror(errno));
                close(client_socket);
                client_socket = -1;
                we_work = -1;
                continue;
                
            }
            else{
                fprintf( stderr, "%s\n", strerror(errno));
                exit(1);
            }
	    }

        fsize = be64toh(fsize);
        
        //printf("fsize is: %lu\n", fsize);

        /*memset(data_buff, 0,sizeof(data_buff));
        strncpy(data_buff, "got", 4);
        temp = write(client_socket, data_buff, sizeof(data_buff));*/


        //now we read the data send us by the client

        total_read = 0;
        total_printable = 0;
        
        //printf("we start read\n");

        // keep looping until nothing left to read
        while( total_read <fsize ){
            // notwritten = how much we have left to write
            // totalsent  = how much we've written so far
            // nsent = how much we've written in last write() call */
            nsent = read(client_socket, data_buff, sizeof(data_buff));

            if(nsent<0){// check if error occured (client closed connection?)
                fprintf( stderr, "%s\n", strerror(errno));
                break;
            }
            //printf("Server: wrote %d bytes\n", nsent);
            for(int i=0; i<nsent; i++){
                if(is_printable_and_update(data_buff[i])){
                    total_printable++;
                    the_updator[data_buff[i]-shifting]++;
                }
            }

            total_read  += nsent;
            
            //printf("total_read is: %lu\n", total_read);
            
        }//end of while

        if(nsent<0){// check if error occured (client closed connection?)
            close(client_socket);
            client_socket = -1;
            we_work = -1;
            break;
        }
        
        //printf("total printable is: %d\n", total_printable);

        fsize = htobe64(total_printable);
        total_read = 0;

        temp = 1;
        while(temp > 0){ 
		    temp = write(client_socket, for_fsize+total_read, 8-total_read);

		    total_read += temp;
	    }
        if(temp < 0){ 
            if (errno == ETIMEDOUT || errno == ECONNRESET || errno == EPIPE){
                fprintf(stderr, "%s\n", strerror(errno));
                close(client_socket);
                client_socket = -1;
                we_work = -1;
                continue;
            }
            else{
                fprintf(stderr, "%s\n", strerror(errno));
                exit(1);
            }
	    }
        if(total_read != 8){ // client process killed unexpectedly
                fprintf(stderr, "%s\n", strerror(errno));                               
                close(client_socket);
                we_work = -1;
                client_socket = -1;
                continue;
         }
        

        memset(data_buff, 0,sizeof(data_buff));
        //memset(ret_printable, 0,sizeof(ret_printable));
        /*sprintf(ret_printable, "%d", total_printable);
        strcpy(data_buff, ret_printable);
        temp = write(client_socket, data_buff, sizeof(data_buff));*/

        for(int i = 0; i < 95; i++){
            counter_arr[i].counter_of_use += the_updator[i];
        }
        
        //printf("we close\n");

        close(client_socket);// close socket

        client_socket = -1;
        we_work = -1;

    }//end of while

    print_res();

    if(temp>0){//for compile
        temp++;
    }
    
    return 0;

}//end of function main
