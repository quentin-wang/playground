#include <stdio.h>
#include <iostream>
#include <unistd.h>  
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdlib.h>
#include <errno.h>

#define MY_SHM_ID 0x123456

#define MEM_SIZE  (512 * 1024)

void get_buf(float *buf)
{
    int i=0;
    for (i = 0; i < MEM_SIZE / 4; i++)
        buf [i] = i * 2;
}

int main(  )
{
    printf("page size=%d\n", getpagesize());
    int shmid=0, ret=0;
    shmid = shmget(MY_SHM_ID, MEM_SIZE, 0666|IPC_CREAT);
    
    if (shmid > 0)
    {
        printf("Create a shared memory segment %d\n", shmid);
    }
    struct shmid_ds shmds;
    ret = shmctl( shmid, IPC_STAT, &shmds );

    if (ret == 0 )
    {
        printf( "Size of memory segment is %d \n", (int)shmds.shm_segsz );
        printf( "Number of attaches %d \n", (int)shmds.shm_nattch );
    }
    else
    {
        printf( "shmctl () call failed \n");
    }
    
    // write data to share memary
    char *buf = NULL;
    if ((int)(buf=(char*)shmat(shmid, NULL, 0)) == -1)
    {
        perror("Share memary can't get pointer\n");
            exit(1);
    }
    get_buf((float *)buf);

    // ret = shmctl(shmid, IPC_RMID, 0);
    
    if (ret == 0)
    {
        printf("Shared memary removed \n");
    }
    else
    {
        printf("Shared memory remove failed \n");
    }
    
    return 0;
}

