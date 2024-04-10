#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

struct Node *head;

void insertBegining(int x) {
    Node *temp = (Node *)malloc(sizeof(struct Node));
    temp->data = x;
    if (head != NULL) {
        temp->next = head;
    }
    head = temp;
};

void printNode() {
    Node *temp = head;
    printf("The list: ");
    while (temp != NULL) {
        printf(" %d", temp->data);
        temp = temp->next;
    }
    printf("\n");
}
int main() {
    head = NULL;
    printf("How many numbers?\n");
    int n, x;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        printf("Enter number: ");
        scanf("%d", &x);
        insertBegining(x);
        printNode();
    }
    return 0;
}
