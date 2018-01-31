#include <stdio.h>   // for putchar, fflush, stdout, printf
#include <stdlib.h>  // for rand, srand
#include <assert.h>  // for assert
#include <string.h>  // for strlen
#include <unistd.h>  // for fork, sleep
#include <sys/sem.h> // for sumbuf, semget, semctl, semop
 
#define KEY 0x1111
 
union semun {
    int val;
    struct semid_ds *buf;
    unsigned short *array;
};
 
static struct sembuf p = { 0, -1, SEM_UNDO };
static struct sembuf v = { 0, +1, SEM_UNDO };
 
int main(void)
{
    // semget
    int id = semget(KEY, 1, 0666 | IPC_CREAT);
    assert(id >= 0 && "semget failed");
 
    // semctl
    union semun u;
    u.val = 1;
    assert(semctl(id, 0, SETVAL, u) >= 0);
 
    int pid;
    pid = fork();
 
    assert(pid >= 0 && "fork failed");
 
    const char *s;
    if (pid)
        s = "abcdefgh";
    else
        s = "ABCDEFGH";
 
    srand((unsigned int)pid);
    for (size_t i = 0; i < strlen(s); ++i)
    {
        // semop
        assert(semop(id, &p, 1) >= 0);
 
        putchar(s[i]);
        fflush(stdout);
        sleep(rand() % 2);
       
        putchar(s[i]);
        fflush(stdout);
        sleep(rand() % 2);
 
        // semop
        assert(semop(id, &v, 1) >= 0);
    }
 
    sleep(3);
    printf("\n-- %d DONE --\n", pid);
 
    return 0;
}
