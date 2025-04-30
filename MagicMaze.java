import java.util.ArrayList;
import java.util.List;

public class ConstraintSolver {

    List<String> constraints = new ArrayList<>();
    boolean equal = false;

    public void Solver(int[][]arr, int n, int d){
        int i, j;
        for(i=0;i<n;i++){
            for(j=i+1;j<d;j++){ //upper triangle only
                if(arr[i][j]==1){
                    //connected, add adjacency constraint x-y >1
                    //addAdjacencyConstraints(i,j);


                }
                if(i == j){
                    //disequality constraint x!=y
                    //addDisequalityConstraints(i,j);
                    equal = false;
                    break;


                }
            }
        }

//        for(int x=arr[0].length ; x<n; x++){
//            for(int y=arr.length; y<d; y++){
//                boolean constr;
//                if (x-y >1){
//                    constr = true;
//
//                }
//            }
//        }
    }

//    public void addDisequalityConstraints(int i, int j) {
//        constraints.add()
//
//    }

    public void addAdjacencyConstraints(int i, int j) {

    }

}

