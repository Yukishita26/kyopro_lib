
#include <iostream>
#include <cassert>
using namespace std;
class UnionFindTree{
    private:
    int tree[10007];
    int rank[10007];
    public:
    UnionFindTree(int N){
        for(int i=0; i<=N; i++){
            tree[i] = i;
            rank[i] = 1;
        }
    }
    int root(int a){
        if (tree[a] == a) return a;
        return (tree[a] = root(tree[a]));
    }
    bool is_same_set(int a, int b){
        return root(a) == root(b);
    }
    void unite(int a, int b){
        int ra = root(a);
        int rb = root(b);
        if(ra == rb) return;
        if(rank[ra] < rank[rb]){
            tree[ra] = rb;
        }else{
            tree[rb] = ra;
            if(rank[ra] == rank[rb]){
                rank[ra]++;
            }
        }        
    }
};
void test(){
    auto uft = UnionFindTree(10);
    assert(! uft.is_same_set(1, 3));
    uft.unite(1, 2);
    assert(! uft.is_same_set(1, 3));
    uft.unite(2, 3);
    assert(uft.is_same_set(1, 3));
}
int main(){
    test();
}