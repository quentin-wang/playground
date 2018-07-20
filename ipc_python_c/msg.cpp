#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <errno.h>
#include <string.h>

#define MSG_TEXT_SIZE   8
struct ipc_msg {
    long int type;
    char buf [MSG_TEXT_SIZE];
};

#define MSG_KEY 0x1001
#define MY_MSG_TYPE 0x02

int main(int argc, char const *argv[])
{
    /* code */
    int i = 0;
    /* create msg queue*/
    struct ipc_msg some_msg;
    some_msg.type = MY_MSG_TYPE;
    memcpy(some_msg.buf, "This is a test", sizeof(some_msg.buf)); 

    int msgid = msgget((key_t)MSG_KEY, 0666|IPC_CREAT);
    if (msgid == -1)
    {
        fprintf(stderr, "msgget failed: %d \n", errno);
        exit(EXIT_FAILURE);
    }

    while (1)
    {
        if (msgsnd(msgid, (void *) &some_msg, MSG_TEXT_SIZE, 0) == -1)
        {
            fprintf(stderr, "msgsnd failed: %d \n", errno);
            exit(EXIT_FAILURE);
        }
        break;
    }

    // msgrcv(msgid, (void *) &some_msg, sizeof (some_msg), MY_MSG_TYPE, 0);
    // for (i = 0; i < MSG_BUF_SIZE; i++)
    //     printf("%c", some_msg.buf[i]);
        
    // if (msgctl(msgid, IPC_RMID, 0) == -1)
    // {
    //     fprintf(stderr, "msgctl delete failed: %d \n", errno);
    //     exit(EXIT_FAILURE);
    // }

    return 0;
}

