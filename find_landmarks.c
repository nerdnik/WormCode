#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <popt.h>
#include <assert.h>
#include <omp.h>
#include <sys/time.h>
#include <sys/types.h>



/*===============================================
From CSCI5576 HW7
===============================================*/
double calctime(struct timeval start, struct timeval end) 
{
  double time = 0.0;
  time = end.tv_usec - start.tv_usec;
  time = time/1000000;
  time += end.tv_sec - start.tv_sec;

  return time;
}

/*===============================================
End from CSCI5576 HW7
===============================================*/

// Example of basic command line run after compilation:
//	./find_landmarks -i {witness input file} -o {file to output landmarks & distances} -l {number of landmarks} -w 0-100 
// for more information on parameters in the command line type ./find_landmarks --help



/*=============================================================
        Samantha Molnar
		Calculate euclidean distance matrix of witnesses then landmark selection.
=============================================================*/
typedef enum { false, true } bool; // Provide C++ style 'bool' type in C
float           *witnesses;
float           *distances;
float           *euc_distance;
float           *times;
float           *velocities;
float           *norm_velocity;
float           *speeds;
float           *cov_matrices;
//timing
float            avg_time;
float            dev;
float            err;
float            sum;

//used to store calculated values
float            x,y,x1,yone,x2,y2,d,r,s,m,xi,xj,yi,yj; 
float            min_speed=1000000;
float            max_speed=-1000000;


//distance calculation options
float            use_hamiltonian = 0.0;
float            speed_amplify = 1.0;
float            orientation_amplify = 1.0;
float            ray_distance_amplify = 1.0;
float            straight_VB=0.0;
float            stretch = 1.0;


char            *file;
char            *wfile;
char            *wit;
char            *landmark_set;
FILE            *fp;

int64_t          num_wits=1;
int64_t          i,j,k;
int              knn = 7;  //k nearest neighbors
int              m2_d = 0.0;
int              num_landmarks=1;
int              t,l;
int              est;
int              start=0;
int              stop=1;
int              num_threads = 4;
int              d_cov = 0;

int              max_avg=50;
int              wit_pts=2; 
int             *landmarks;

bool             use_est=false;
bool             alt_wit=false;
bool             timing=false;

bool             use_euclidean = false;
bool             done = false;
bool 			 quiet = true;

void dprint(char *c);
void print_matrix(float *A);
float std_dev(float d[],int s);
float calc_error(float d,int n);
float e_dist(float,float,float,float);
bool in_matrix(int* matrix,int size,int value);
int main(int argc, char* argv[]){
        char *parse;
	struct timeval begin;
	struct timeval end;
  /***************** Command line argument parsing  *************************/
poptContext POPT_Context;  /* context for parsing command-line options */
  char        POPT_Ret;      /* used for iterating over the arguments */

  struct poptOption optionsTable[] =
  { 
    { "input file",                'i', POPT_ARG_STRING,     &file,                1, "Input file of witnesses",                                              0 },
    { "output file",               'o', POPT_ARG_STRING,     &wfile,               2, "Where to output landmarks and their distances to each witness.",       0 },
    { "landmarks",                 'l', POPT_ARG_INT,        &num_landmarks,       3, "Number of landmarks to use.",                                          0 },
    { "witnesses",                 'w', POPT_ARG_STRING,     &parse,               4, "Number of witnesses to use.  Can be an integer or a range of integers like x-y",      0 },
    { "evenly spaced in time",     'e', POPT_ARG_INT,        &est,                 5, "Use evenly spaced in time to select every x landmark.",                0 },
    { "time program",              't', POPT_ARG_NONE,       0,                    6, "Time each step of the code and output results.",                       0 },
    { "print everything",          'q', POPT_ARG_NONE,       0,                    7, "Print all output.  Use for debugging.",                                0 },
    { "set speed amplify",         'a', POPT_ARG_FLOAT,      &speed_amplify,       8, "Set the speed amplify variable.",                                      0 },
    { "set orientation amplify",   'y', POPT_ARG_FLOAT,      &orientation_amplify, 9, "Set the orientation amplify variable.",                                0 },
    { "set use hamiltonian",       'h', POPT_ARG_FLOAT,      &use_hamiltonian,    10, "Set the use hamiltonian variable.",                                    0 },
    { "set m2_d",                  'm', POPT_ARG_INT,        &m2_d,               11, "Set the m2_d variable.",                                               0 },
    { "set ray dist amplify",      'r', POPT_ARG_FLOAT,      &speed_amplify,      12, "Set the ray distance amplify variable.",                               0 },
    { "number of threads",         'n', POPT_ARG_INT,        &num_threads,        13, "Set the number of threads to use.",                                    0 },
    { "set straight_VB",           'v', POPT_ARG_FLOAT,      &straight_VB,        14, "Set the straight_VB variable.",                                        0 },
    { "set stretch ",              's', POPT_ARG_FLOAT,      &stretch,            15, "Set the stretch variable.",                                            0 },
    { "use euclidean ",            'c', POPT_ARG_NONE,       0,                   16, "Calculate distance using euclidean distance.",                         0 },
    { "cov",                       'x', POPT_ARG_INT,        &d_cov,              17, "Calculate distance using covariance.",                                 0 },
    POPT_AUTOHELP
    { NULL, '\0', 0, NULL, 0}
  };
  POPT_Context = poptGetContext(NULL, argc, (const char**) argv, optionsTable, 0);
  poptSetOtherOptionHelp(POPT_Context, "[ Try --help for a more detailed description of the options]");
   /* values are filled into the data structures by this function */
   while ((POPT_Ret = poptGetNextOpt(POPT_Context)) >= 0)
   {
     switch (POPT_Ret) 
     {
      case 1:
        if(!quiet)
        	printf("Input file:%s\n",file);
        break;
      case 2:
      	if(!quiet)
        	printf("Output file:%s\n",wfile);
        break;
      case 3:
      	if(!quiet)
        	printf("Number of landmarks set to %d.\n",num_landmarks);
        	fflush(stdout);
        break;
      case 4:
        if(strchr(parse,'-')!=NULL){
        	parse=strtok(parse,"-");
        	i=0;
        	while(parse!=NULL){
            
            if(i==0)
            	start = atoi(parse);
            else
            	stop = atoi(parse);
            i++;
            parse=strtok(NULL,",-");
          }
        }
		else{
            start = 0;
            stop = atoi(parse);
        }
				
				num_wits = stop-start;
				printf("Number of witnesses: %d\n",num_wits);
				fflush(stdout);
				break;
      case 5:
      	use_est=true;
      	if(!quiet)
      	printf("Using evenly spaced in time to find landmarks.\n");
		break;
      case 6:
      	if(!quiet)
      		printf("Timing selection processes.\n");
		timing = true;
		break;
	  case 7:
	  	quiet = false;
	  	break;
	  case 13:
	  	printf("Number of threads: %d\n",num_threads);
	  	break;
	  case 16:
	  	if(!quiet)
	  		printf("Using euclidean distance.\n");
	  	use_euclidean = true;
	  	break;
	  case 17:
	  	printf("Calculating distance with covariance matrix.\n");
    }
  }
  if (POPT_Ret < -1) 
  {
    /* an error occurred during option processing */
    fprintf(stderr, "%s: %s\n",
    poptBadOption(POPT_Context, POPT_BADOPTION_NOALIAS),
    poptStrerror(POPT_Ret));
    return 1;
  }
  poptFreeContext(POPT_Context);
  /***************** End command line parsing *************************/



	witnesses         = (float*) calloc(num_wits*wit_pts,sizeof(float));// x,y points for a witness
	distances         = (float*) calloc((float)num_wits*(float)num_wits,sizeof(float)); //distance between all witnesses
	euc_distance      = (float*) calloc((float)num_wits*(float)num_wits,sizeof(float)); //distance between all witnesses
	landmarks         = (int*)   calloc(num_landmarks,sizeof(int));//landmark set
	times             = (float*) calloc(max_avg,sizeof(float));//used for timing results
	velocities        = (float*) calloc(num_wits*wit_pts,sizeof(float));//velocities of witnesses
	norm_velocity     = (float*) calloc(num_wits*wit_pts,sizeof(float));//normalized velocities of witnesses
	speeds            = (float*) calloc(num_wits,sizeof(float)); //speeds of witnesses
	landmark_set      = (char*)  calloc(num_wits,sizeof(char)); //set of chosen landmarks
	cov_matrices      = (float*) calloc(num_wits*wit_pts*wit_pts,sizeof(float));
	float fx,fy;
	i = 0;
	j = 0;
	/**************** Putting data into data structures ****************/
	fp=fopen(file,"r");
	if (fp == NULL) {
    	perror("Failed: ");
    	return 1;
	}
	printf("Reading in witnesses...");

	fflush(stdout);
	

	//reading in witnesses from file
	
	l = 0;
	i=0;
	while(l<stop){
		fscanf(fp,"%f %f",&fx,&fy);	

		if(l>=start){ 
			witnesses[i*wit_pts]=fx;
			witnesses[i*wit_pts+1]=fy;
			landmark_set[l] = 'n';
			i++;
		}
		l++;
	}

	if(!quiet) //this is a debugging statement
		printf(" %d/%d witnesses read...",l,num_wits);
	fclose(fp);
	fp=NULL;

	printf("done\n");
	fflush(stdout);
	//calculating velocities
	float vx,vy;
	printf("Calculating vectors...");
	fflush(stdout);
	for(i=0;i<num_wits-1;i++){
		vx = (witnesses[i*wit_pts+wit_pts]-witnesses[i*wit_pts]);
		vy = (witnesses[i*wit_pts+1+wit_pts]-witnesses[i*wit_pts+1]);
		velocities[i*wit_pts] = vx;
		velocities[i*wit_pts+1]=vy;
	}

	//Last one's velocity is just copy of second to last one's velocity.

	velocities[num_wits*wit_pts-wit_pts] = velocities[(i-1)*wit_pts];
	velocities[num_wits*wit_pts-1] = velocities[(i-1)*wit_pts+1];
	
	//calculating speeds
	for(i=0;i<num_wits-1;i++){
		speeds[i]=sqrt(velocities[i*wit_pts]*velocities[i*wit_pts]+velocities[i*wit_pts+1]*velocities[i*wit_pts+1]);
		if(speeds[i]>max_speed)
			max_speed = speeds[i];
		if(speeds[i]<min_speed)
			min_speed = speeds[i];
	}
	speeds[num_wits-1] = speeds[num_wits-2];
	j=0;
	for(i=0;i<num_wits-1;i++){
		norm_velocity[i*wit_pts] = velocities[i*wit_pts]/speeds[j];
		norm_velocity[i*wit_pts+1] = velocities[i*wit_pts+1]/speeds[j];
		j++;
	}
	
	
	norm_velocity[num_wits*wit_pts-wit_pts] = norm_velocity[(i-1)*wit_pts];
	norm_velocity[num_wits*wit_pts-1] = norm_velocity[(i-1)*wit_pts+1];

	printf("done\n");
	fflush(stdout);

/*******************************************************************/

/***************** Calculating distance matrix ********************/

	
	if(use_euclidean){
		
		t = 0;
		bool done = false;
		if(timing){
			printf("Running distance calculations 1 with");
			while(!done && t<max_avg){// run this multiple times to get a better value for the average time
	  		#pragma omp parallel num_threads(num_threads) shared(distances,witnesses,num_wits,wit_pts) private(i,j,x,y)
	  		{	
			/************************************************/	
					if(omp_get_thread_num()==0 && t==0){
						printf(" %d threads..",omp_get_num_threads());
						fflush(stdout);
					}
					gettimeofday(&begin,NULL);
					#pragma omp for nowait schedule (runtime)
					for(i=0;i<num_wits;i++){		
						for(j=0;j<num_wits;j++){
							x = witnesses[i*wit_pts]-witnesses[j*wit_pts];
							x = x*x;
							y = witnesses[i*wit_pts+1]-witnesses[j*wit_pts+1];
							y = y*y;
							distances[i*num_wits+j] = sqrt(x+y);
						}
					}
					gettimeofday(&end,NULL);
					printf("Thread %d took %f to do work\n",omp_get_thread_num(),calctime(begin,end));	
      	    /************************************************/
	    	}
	  		times[t] = calctime(begin,end);
	  		t++;
	  		dev = std_dev(times,t);
	  		err = calc_error(dev,t);
	  		if(err<=.1 && t>=2)
	      	done = true;
			}
			printf("done\n");
			sum = 0.0;
			for(i = 0; i<t;i++){
	  		sum+=times[i];
	  		times[i]=0;
			}
			printf("\tDistance matrix of size %lld took %f (s) with an error of %f.\n",num_wits,sum/(float)t,err);
		}
		else{//not timing
			printf("Running distance calculations 2..."); //euclidean
			fflush(stdout);
			#pragma omp parallel num_threads(num_threads) shared(distances,witnesses,num_wits,wit_pts) private(i,j,x,y)
			{
				#pragma omp for nowait schedule (runtime)
				for(i=0;i<num_wits;i++){		
					for(j=0;j<num_wits;j++){
						x = witnesses[i*wit_pts]-witnesses[j*wit_pts];
						x = x*x;
						y = witnesses[i*wit_pts+1]-witnesses[j*wit_pts+1];
						y = y*y;
						distances[i*num_wits+j] = sqrt(x+y);
					}
				}	
			}

		}

	}
	else{

		#pragma omp parallel num_threads(num_threads) shared(euc_distance,witnesses,num_wits,wit_pts) private(i,j)
		{
			#pragma omp for nowait schedule (runtime)
			for(i=0;i<num_wits;i++){		
				for(j=0;j<num_wits;j++){
					euc_distance[i*num_wits+j] = e_dist(witnesses[i*wit_pts], witnesses[i*wit_pts+1], witnesses[j*wit_pts], witnesses[j*wit_pts+1]);
				}
			}	
		}
	}


	if(use_hamiltonian!=0.0){ //hamiltonian is something other than 0
		printf("Running distance calculations 3...");
		fflush(stdout);
		float dhamil=0.,deuc=0.;
		if(use_hamiltonian<0){
		
			#pragma omp parallel num_threads(num_threads) shared(euc_distance,num_wits,witnesses,use_hamiltonian,norm_velocity,straight_VB,distances,wit_pts) private(i,j,deuc,dhamil)
			{
				#pragma omp for nowait schedule (runtime)
				for(i=0;i<num_wits;i++){
					for(j=0;j<num_wits;j++){
						deuc = euc_distance[i*num_wits+j];
						dhamil = -1*use_hamiltonian*e_dist(norm_velocity[i*wit_pts],norm_velocity[i*wit_pts+1],norm_velocity[j*wit_pts],norm_velocity[j*wit_pts+1]);
						distances[i*num_wits+j] = sqrt(deuc*deuc+(dhamil*dhamil));
					}
				}
			}
		}

		else{
			#pragma omp parallel num_threads(num_threads) shared(euc_distance,num_wits,witnesses,use_hamiltonian,norm_velocity,straight_VB,distances,wit_pts) private(i,j,deuc,dhamil)
			{
				#pragma omp for nowait schedule (runtime)
				for(i=0;i<num_wits;i++){
					for(j=0;j<num_wits;j++){
						deuc = euc_distance[i*num_wits+j];
						dhamil = use_hamiltonian*e_dist(velocities[i*wit_pts],velocities[i*wit_pts+1],velocities[j*wit_pts],velocities[j*wit_pts+1]);
						distances[i*num_wits+j] = sqrt(deuc*deuc+(dhamil*dhamil));
					}
				}
			}
		}
	}

	else if(m2_d!= 0.0){
		printf("Running distance calculations 4..."); //m2_d
		fflush(stdout);
		float d1,d2;
			#pragma omp parallel num_threads(num_threads) shared(euc_distance,witnesses,num_wits,distances) private(i,j,d1,d2)
			{
				#pragma omp for nowait schedule (runtime)
				for(i=0;i<num_wits;i++){		
					for(j=0;j<num_wits;j++){
						d1=euc_distance[i*num_wits+j];
						d2=euc_distance[(i+1)*num_wits+(j+1)];
						distances[i*num_wits+j]= sqrt(d1*d1+d2*d2);	
					}
				}
			}
			
	}
	else if(d_cov!=0){
		printf("Running distance calculations 5...\n"); // covariance
		if(d_cov<0){//distance from mean of k nearest neighbors to k nearest neighbors
			d_cov*=-1;
			int neighbors[d_cov];
			float ndist[d_cov];
			
			int found = 0;
			float min = 88888;
			int min_index = -1;
			float mean[wit_pts];
			float sum=0;

			#pragma omp parallel num_threads(num_threads) shared(d_cov,num_wits,witnesses,euc_distance,wit_pts) private(i,j,k,l,min,min_index,neighbors,ndist,found,mean,sum)
			{
				#pragma omp for nowait schedule (runtime)
				for(i=0;i<num_wits;i++){
					found = 0;
					mean[0]=0;
					mean[1]=0;

					//find nearest neighbors
					while(found<d_cov){
						min = 8888888;
						min_index = -1;
						for(j=0;j<num_wits;j++){
							if(euc_distance[i*num_wits+j]<min && !in_matrix(neighbors,d_cov,j) && j!=i){
								min = euc_distance[i*num_wits+j];
								min_index = j;
							}
						}
						neighbors[found] = min_index;
						ndist[found] = min;
						found++;
					}

					for(j=0;j<d_cov;j++){
						mean[0]+=witnesses[neighbors[j]*wit_pts];
						mean[1]+=witnesses[neighbors[j]*wit_pts+1];
					}
					mean[0]=mean[0]/(float)d_cov;
					mean[1]=mean[1]/(float)d_cov;
					
					
					
					//calculate covariance matrix
					
					for(j=0;j<wit_pts;j++){
						for(k=0;k<wit_pts;k++){
							sum = 0;
							for(l=0;l<d_cov;l++){
								sum+=(witnesses[neighbors[l]*wit_pts+j]-mean[j])*(witnesses[neighbors[l]*wit_pts+k]-mean[k]);
							}
							cov_matrices[(i*wit_pts*wit_pts)+j*wit_pts+k] = sum/((float)d_cov-1);
						}
					}
				}
			}

		}


		else{ //instead of using mean closest witness use closest witness

			int neighbors[d_cov];
			float ndist[d_cov];
			
			int found = 0;
			float min = 88888;
			int min_index = -1;
			float closest[wit_pts];
			float sum=0;

			#pragma omp parallel num_threads(num_threads) shared(d_cov,num_wits,witnesses,euc_distance,wit_pts) private(i,j,k,l,min,min_index,neighbors,ndist,found,closest,sum)
			{
				#pragma omp for nowait schedule (runtime)
				for(i=0;i<num_wits;i++){
					found = 0;
					closest[0]=0;
					closest[1]=0;

					//find nearest neighbors
					while(found<d_cov){
						min = 8888888;
						min_index = -1;
						for(j=0;j<num_wits;j++){
							if(euc_distance[i*num_wits+j]<min && !in_matrix(neighbors,d_cov,j) && j!=i){
								min = euc_distance[i*num_wits+j];
								min_index = j;
							}
						}
						neighbors[found] = min_index;
						ndist[found] = min;
						found++;
					}
					min= 888888;
					min_index = -1;
					for(j=0;j<d_cov;j++){
						if(ndist[j]<min){
							min = ndist[j];
							min_index = neighbors[j];
						}
					}
					closest[0]=witnesses[neighbors[min_index]*wit_pts];
					closest[1]=witnesses[neighbors[min_index]*wit_pts+1];
					
					
					
					//calculate covariance matrix
					
					for(j=0;j<wit_pts;j++){
						for(k=0;k<wit_pts;k++){
							sum = 0;
							for(l=0;l<d_cov;l++){
								sum+=(witnesses[neighbors[l]*wit_pts+j]-closest[j])*(witnesses[neighbors[l]*wit_pts+k]-closest[k]);
							}
							cov_matrices[(i*wit_pts*wit_pts)+j*wit_pts+k] = sum/((float)d_cov-1);
						}
					}
				}
			}
		}


		//now calculate distance using covariance d(w_i,w_j) = [w_i]*cov(w_i)*[w_j]

		float c0,c1;
		#pragma omp parallel num_threads(num_threads) shared(distances,cov_matrices,witnesses,wit_pts,num_wits) private(i,j,c0,c1)
		{
			#pragma omp for nowait schedule (runtime)
			for(i=0;i<num_wits;i++){
				for(j=0;j<num_wits;j++){
					c0 = witnesses[i*wit_pts] - witnesses[j*wit_pts];
					c1 = witnesses[i*wit_pts+1] - witnesses[j*wit_pts+1];
					distances[i*num_wits+j] = c0*c0*cov_matrices[(i*wit_pts*wit_pts)] + c0*c1+cov_matrices[(i*wit_pts*wit_pts)+1] + c0*c1+cov_matrices[(i*wit_pts*wit_pts)+2] + c1*c1+cov_matrices[(i*wit_pts*wit_pts)+3];
				}
			}
		}

	}
	
	else if(orientation_amplify!=1){
		float de,dot;
		printf("Running distance calculations 6..."); //orientation
		fflush(stdout);
		#pragma omp parallel num_threads(num_threads) shared(num_wits,witnesses,stretch,norm_velocity,orientation_amplify,speeds,min_speed,max_speed,speed_amplify,distances,straight_VB) private(i,j,de,dot)
		{
			#pragma omp for nowait schedule (runtime)
			for(i=0;i<num_wits;i++){
				for(j=0;j<num_wits;j++){
					dot = orientation_amplify*(norm_velocity[i*wit_pts]*norm_velocity[j*wit_pts]+norm_velocity[i*wit_pts+1]*norm_velocity[j*wit_pts+1]+1)/2.;
					de = e_dist(witnesses[i*wit_pts],witnesses[i*wit_pts+1],witnesses[j*wit_pts],witnesses[j*wit_pts+1]);
					distances[i*num_wits+j] = de/(dot+1.); 			
				}
			}
		}
	}

/******************************************************************/

	printf("done\n");
	fflush(stdout);

	


/********************* Determing landmark set *********************/
	if(!use_est){
		landmark_set[0]='l';
		landmarks[0]=0;
		printf("Determining landmark set using MaxMin...",num_threads);
		fflush(stdout);
		float   max=-1,min=888888888,dist;
		int     max_index,landmark,min_index,l_count=1;
		int     candidate_set[num_wits];
		float   candidate_dist[num_wits];

		while(l_count<num_landmarks){
			#pragma omp parallel num_threads(num_threads) shared(l_count,witnesses,num_wits,num_landmarks,candidate_set,candidate_dist,landmark_set) private(i,l,min,min_index,max_index,max,dist,landmark) 
			{
				#pragma omp for nowait schedule(runtime)
					for(i=0;i<num_wits;i++){
						min = 888888888;
						min_index = -1;
						if(landmark_set[i]=='n'){
							
							for(l=0;l<l_count;l++){
								landmark = landmarks[l];			
								dist = e_dist(witnesses[landmark*wit_pts],witnesses[landmark*wit_pts+1],witnesses[i*wit_pts],witnesses[i*wit_pts+1]);
								if(dist<min){
									min = dist;
									min_index = i;
								}
							}
						}
						candidate_set[i] = min_index;
						candidate_dist[i] = min;
					}
				#pragma omp master
				{	
					max = 0.;
					max_index = -1;
					for(i=0;i<num_wits;i++){
						if(candidate_dist[i]>max && landmark_set[i]!='l'){
							max = candidate_dist[i];
							max_index = i;
						}
					}
					landmarks[l]=max_index;
					landmark_set[max_index] = 'l';
					l_count+=1;
				}
				#pragma omp barrier
				
		  	}
		}
		
		printf("done\n");
		fflush(stdout);
	}

	else{

		printf("Determining landmark set using evenly spaced in time with downsample of %d...",est);
		
		fflush(stdout);

		k=0;
		for(i=0;i<num_wits;i++){
			if((i+1)%est==0 && k<num_landmarks){
				landmarks[k] = i; 
				landmark_set[i] = 'l';
				k++;
			}
		}
		printf("done\n");
	}
/******************************************************************/


/************* Writing landmarks distances to file ****************/
	printf("Writing landmarks to file...");
	fflush(stdout);
	fp=fopen("landmark_outputs.txt","w");
	if (fp == NULL) {
    	printf("\n\n\t\t ERROR: Failed to open output file %s!\n",wfile);
    	fflush(stdout);
    	return 1;
	}
	fprintf(fp,"#landmark: d(l,w1), d(l,w2) ... d(l,w_n) where l refers to the landmark's occurence in the witness file, order of the list refers to order it was found\n");
	
	for(i=0;i<num_landmarks;i++){
		fprintf(fp,"%d: ",landmarks[i]);
    	
		for(j=0;j<num_wits;j++){
			if(j<num_wits-1)
			{
				
				fprintf(fp,"%f, ",distances[landmarks[i]*num_wits+j]);
			}
			else
			{
				fprintf(fp,"%f\n",distances[landmarks[i]*num_wits+j]);
			}
		}
	}
	
	fclose(fp);
	printf("done\n");
	fflush(stdout);
	
/******************************************************************/

	printf("Freeing memory...");
	fflush(stdout);
	
	//free allocated memory
	free(witnesses);
	free(times);
	free(velocities);
	free(norm_velocity);
	free(speeds);
	free(landmark_set);
	free(distances);
	free(euc_distance);
	free(landmarks);
	free(cov_matrices);


	printf("done\n");
	fflush(stdout);

	return 0;

}
bool in_matrix(int *matrix, int size,int value){
	int z;
	for(z=0;z<size;z++){
		if(matrix[z]==value)
			return true;
	}
	return false;
}
void print_matrix(float *A){
	for(i=0;i<num_wits;i++){
		for(j=0;j<num_wits;j++){
			printf("%.2f ",A[i*num_wits+j]);
		}
		printf("\n");
	}
}

void dprint(char *c){
	printf("DUBUGGING STATEMENT\t[");
	printf(c);
	printf("]\n");
	fflush(stdout);
}
float e_dist(float ix, float iy, float jx, float jy){
	return sqrt((jx-ix)*(jx-ix)+(jy-iy)*(jy-iy));
}

float std_dev(float d[],int n){
    float sum=0.0;
    int z;
    for(z=0; z<n;z++){
        sum+=d[z];
    }
    float mean=sum/(float)n;
    sum=0.0;
    for(z=0;z<n;z++){
        sum+=(d[z]-mean)*(d[z]-mean);
    }
    return sqrt(sum/(float)n);
}

float calc_error(float dev,int n){
    float e=1.96*dev/(float)sqrt(n);
    return e;
}
