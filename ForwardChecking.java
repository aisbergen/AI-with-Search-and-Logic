import java.util.ArrayList;
import java.util.List;

public class ForwardChecking extends ConstraintSolver {
    ConstraintSolver constraintSolver = new ConstraintSolver() {};

        public boolean reviseAC3(int i, int j) {
            boolean changed = false;
            List<Integer> Di = new ArrayList<>();
            List<Integer> Dj = new ArrayList<>();
            for (int di : Di){
                boolean supported = false;
                while(!supported){
                    for(int dj : Dj ){
                        if(i == di && j==dj){
                            //satisfies c(xi, xj)
                            supported = true;
                        }
                    }
            }
                if(!supported){
                    Di.remove(di);
                    changed = true;
                }

            }

            if(Di.isEmpty()){
                
            }
            return changed;



}}
