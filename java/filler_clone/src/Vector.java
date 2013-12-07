import java.lang.Math;

public class Vector
{	
	private double velocity_x = 0;
	private double velocity_y = 0;
	//private double unit_vector;
	
	/**
	 * Create a vector where all velocities are 0.
	 */
	public Vector ()
	{
	}

	/**
	 * Creates a randomly generated Vector.
	 * 
	 * @param hello_world Any boolean value.
	 */
	public Vector (boolean hello_world)
	{
		this();
		randomise();
	}
	
	/**
	 * Create a new vector with the given velocities.
	 * 
	 * @param vx The x velocity.
	 * @param vy The y velocity.
	 */
	public Vector (double vx, double vy)
	{
		velocity_x = vx;
		velocity_y = vy;
	}
	
	/**
	 * Creates a new vector given two points.
	 * 
	 * @param x_one The x value of point 1.
	 * @param y_one The y value of point 1.
	 * @param x_two The x value of point 2.
	 * @param y_two The y value of point 2.
	 */
	public Vector (double x_one, double y_one, double x_two, double y_two)
	{
		velocity_x = x_one - x_two;
		velocity_y = y_one - y_two;
	}
	
	/**
	 * Accessor for the angle of the vector.
	 * 
	 * @return The angle of the vector in radians.
	 */
	public double get_angle_rad()
	{
		return Math.atan(velocity_x/velocity_y);
	}
	
	/**
	 * Accessor for the angle of the vector.
	 * 
	 * @return The angle the vector is pointing in degrees.
	 */
	public double get_angle_deg()
	{
		return Math.toDegrees(get_angle_rad());
	}
	
	
	public double get_velocity_x()
	{
		return velocity_x;
	}
	
	public double get_velocity_y()
	{
		return velocity_y;
	}
	public void set_velocity_y(double vy)
	{
		velocity_y = vy;
	}
	
	public void reverse_velocity_y()
	{
		velocity_y = - velocity_y;
	}
	
	public void reverse_velocity_x()
	{
		velocity_x = - velocity_x;
	}
	
	public double get_slope()
	{
		return velocity_x / velocity_y;
	}
	
	/**
	 * Returns a new vector with the same velocities.
	 */
	public Vector clone()
	{
		return new Vector(velocity_x, velocity_y);
	}
	/**
	 * Takes the signs from the slope of the other vector and matches these to 
	 * those.  This allows bouncing off another object easily.
	 * 
	 * @param other
	 */
	public void match_signs(Vector other)
	{
		//Get the signs for the x and y velocities as either + or - 1
		double sign_x = other.get_velocity_x() / Math.abs(other.get_velocity_x());
		double sign_y = other.get_velocity_y() / Math.abs(other.get_velocity_y());
		
		//Change the signs of this vector to match the other's
		velocity_x = sign_x * Math.abs(velocity_x);
		velocity_y = sign_y * Math.abs(velocity_y);
	}
	
	/**
	 * Randomises the direction and velocity of the vector.
	 * 
	 * Sets direction and velocity between 0 and 1
	 */
	public void randomise()
	{
		
		velocity_x = -0.05 + Math.random() * 0.1;
		velocity_y = -0.05 + Math.random() * 0.1;
	}
	
	/**
	 * Calculates the dot product of two vectors.
	 * 
	 * @param a The first vector.
	 * @param b The second vector.
	 * @return The dot product of the two vectors.
	 */
	public static double dot_product(Vector a, Vector b)
	{
		return a.velocity_x * b.velocity_x + a.velocity_y * b.velocity_y;
	}
	
	/**
	 * Calculates the dot product of this vector and another.
	 * 
	 * @param b The other vector.
	 * @return The dot product of this vector and the supplied one.
	 */
	public double dot_product(Vector b)
	{
		return dot_product(this, b);
	}
	
	/**
	 * Normalizes this vector.
	 * 
	 */
	public void normalize()
	{
		velocity_x /= Math.sqrt (velocity_x*velocity_x + velocity_y*velocity_y);
		velocity_y /= Math.sqrt (velocity_x*velocity_x + velocity_y*velocity_y);
	}
	
	public void subtract(Vector other)
	{
		velocity_x = velocity_x - other.get_velocity_x();
		velocity_y = velocity_y - other.get_velocity_y();
	}
	
	public void multiply(double constant)
	{
		velocity_x *= constant;
		velocity_y *= constant;
	}
	
	public void add(Vector other)
	{
		velocity_x += other.get_velocity_x();
		velocity_y += other.get_velocity_y();
	}
	/**
	 * Adds a number of units to the current x location and
	 * returns a new location based off the velocity of the 
	 * vector.
	 * 
	 * @param current_x  The current x position of an object.
	 * @return The new x position.
	 */
	public double get_new_position_x(double current_x)
	{
		return velocity_x + current_x;
	}

	/**
	 * Adds a number of units to the current y location and
	 * returns a new location based off the velocity of the
	 * vector.
	 * 
	 * @param current_y  The current y position of an object.
	 * @return The new y location.
	 */
	public double get_new_position_y(double current_y)
	{
		return velocity_y + current_y;
	}
	
	//Provides a formatted output for sys.out rather than a fake pointer.
	public String toString()
	{
		return "Velocity X: "+velocity_x+" Velocity y: "+velocity_y;
	}
}
