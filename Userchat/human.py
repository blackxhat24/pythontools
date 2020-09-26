class Human:
    #init fungsi yang dijalankan blueprint (atribute) parameter pertama refer diri sendiri 
    def __init__(self, nama, umur):
        self.nama = nama
        self.umur = umur


"""
class Human
     |
struct Human{
    char nama[]
    int umur
    variable
    Human *next,*prev,*left,*right
}

def __init__(self, nama, umur)
            |
Human *newNode(char *nama, int umur){
    Human *temp = (Human *)malloc*(sizeof(Human))
    strcpy(temp->nama,nama)
    temp->umur = umur
}
"""