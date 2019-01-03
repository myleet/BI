# CUDA templates
class Sub
{
public:
	__device__
	float
		 operator() (float a, float b)
		 const
		 {  
		   return a - b;
		 }
};
class Add
{
public:
	__device__
	float
		 operator() (float a, float b)
		 const
		 {  
		   return a + b;
		 }
};
