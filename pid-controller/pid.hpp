
typedef struct {
//Controller gains
float kp;
float ki;
float kd;

//output limit
float minLimit;
float maxLimit;

//sample time (seconds)
float T;

//memory needed for integrator and differentiator
float integrator;
float differentiator;
float prevError;
float prevMeasure;

//output of controller
float output;
}
