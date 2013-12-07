using System;
using Gtk;

public partial class MainWindow : Gtk.Window
{
	public MainWindow () : base(Gtk.WindowType.Toplevel)
	{
		Build ();
	}

	protected void OnDeleteEvent (object sender, DeleteEventArgs a)
	{
		Application.Quit ();
		a.RetVal = true;
	}
	protected virtual void solveTriangle (object sender, System.EventArgs e)
	{
		try
		{
			string method = "";
			double A,B,C,a,b,c; 
			
			double.TryParse(angleA.Text, out A);
			double.TryParse(angleB.Text, out B);
			double.TryParse(angleC.Text, out C);
			
			double.TryParse(sideA.Text, out a);
			double.TryParse(sideB.Text, out b);
			double.TryParse(sideC.Text, out c);
			
			int numsides = 0;
			int numangles = 0;
						
			if(A != 0)
				numangles++;
			if(B != 0)
				numangles++;
			if(C != 0)
				numangles++;
			
			if(a != 0)
				numsides++;
			if(b != 0)
				numsides++;
			if(c != 0)
				numsides++;
			
			if(numsides == 0)
			{
				MessageDialog md = new MessageDialog(this, 
                DialogFlags.DestroyWithParent, MessageType.Warning, 
                ButtonsType.Close, "Can't solve from angles alone.");
            	md.Run();
            	md.Destroy();
				return;
			}
			
			//Side Side Side
			if(numsides == 3)
			{
				//Solve angles.
				A = cosLawSolveAngle(b, c, a);
  				B = cosLawSolveAngle(c, a, b);
   				C = cosLawSolveAngle(a, b, c);
				
				method = "Side Side Side";
			}
			
			//Angle Side Angle
			else if(numangles >= 2)
			{
				method = "Angle Side Angle";
				
				//Solve angles
				if(numangles == 2)
				{
					if(A != 0 && B != 0)
						C = solveAngles(A, B);
					if(A != 0 && C != 0)
						B = solveAngles(A, C);
					else
						A = solveAngles(B, C);
				}
				
				//Solve sides
				double ratio = 0; // side / sin(angle)
   				if(a != 0)
					ratio = a / Math.Sin( dtor(A) );
				if(b != 0)
					ratio = b / Math.Sin( dtor(B) );
				if(c != 0)
					ratio = c / Math.Sin( dtor(C) );
				
				if(a == 0)
					a = ratio * Math.Sin( dtor(A) );
				if(b == 0)	
					b = ratio * Math.Sin( dtor(B) );
				if(c == 0)
					c = ratio * Math.Sin( dtor(C) );
			}
			/*else if(A != 0 && a != 0 || B != 0 && b != 0 || C != 0 && c != 0) //SAS
			{
				method = "Side Angle Side";
				
				if(a == 0)
					a = cosLawSolveSide(b, c, A);
				if(b == 0)
					b = cosLawSolveSide(c, a, B);
				if(c == 0)
					c = cosLawSolveSide(a, b, C);
				
				if(A == 0)
					A = cosLawSolveAngle(b, c, a);
				if(B == 0)
					B = cosLawSolveAngle(c, a, b);
				if(C == 0)
					C = cosLawSolveAngle(a, b, c);
			}*/
			else
			{ // SSA 
				
				method = "Side Side Angle";
				
				double knownside = 0;
				double knownangle = 0;
				double partialside = 0;
				double partialangle = 0;
				double unknownside = 0;
				double unknownangle = 0;
				double ratio;	
   
   				if(A != 0 && a != 0)
				{
					knownside = a;
					knownangle = A;
				}
				else if(B != 0 && b != 0)
				{
					knownside = b;
					knownangle = B;
				}
				else if(C != 0 && c != 0)
				{
					knownside = c;
					knownangle = C;
				}

   				if(a != 0 && A == 0)
					partialside = a;
				if(b != 0 && B == 0)
					partialside = b;
				if(c != 0 && C == 0)
					partialside = c;
				
				ratio = knownside / Math.Sin( dtor(knownangle) );

				if(partialside / ratio > 1)
				{
					method = "Side Side Angle (No Solution)";
				}
				else if(partialside / ratio == 1 || Math.Asin(partialside / ratio) - dtor( knownangle ) < 0)
				{
					method = "Side Side Angle (One Solution)";
					partialangle = rtod(Math.Asin(partialside / ratio));
				    unknownangle = 180 - knownangle - partialangle;
    				unknownside = ratio * Math.Sin(dtor(unknownangle));
				}
   				else
				{
					method = "Side Side Angle (Two Solutions)";
				}

				if(a != 0 && A == 0)
					A = partialangle;
				if(b != 0 && B == 0)
					B = partialangle;
				if(c != 0 && C == 0)
					C = partialangle;
				
				if(A == 0 && a == 0)
				{
					a = unknownside;
					A = unknownangle;
				}
				if(B == 0 && b == 0)
				{
					b = unknownside;
					B = unknownangle;
				}
				if(C == 0 && c == 0)
				{
					c = unknownside;
					C = unknownangle;
				}
			}

			//Reset Text
			angleA.Text = A.ToString();
			angleB.Text = B.ToString();
			angleC.Text = C.ToString();
			sideA.Text = a.ToString();
			sideB.Text = b.ToString();
			sideC.Text = c.ToString();
			
			methodOutput.Text = method;
		}
		catch( System.FormatException )
		{
			//Some of the numbers didn't work.
			MessageDialog md = new MessageDialog(this, 
                DialogFlags.DestroyWithParent, MessageType.Warning, 
                ButtonsType.Close, "Error parsing input.");
            md.Run();
            md.Destroy();
		}
		
	}
	
	/* Clears the inputs for the program */
	protected virtual void clearTriangle (object sender, System.EventArgs e)
	{
		angleA.Text = "";
		angleB.Text = "";
		angleC.Text = "";
		
		sideA.Text = "";
		sideB.Text = "";
		sideC.Text = "";
		
		methodOutput.Text = "";
	}
	
	/* Completes a remaining angle if two are there. */
	public double solveAngles(double anglea, double angleb)
	{
		return 180 - anglea - angleb;
	}
	
	/*  Returns side c */
	public double cosLawSolveSide(double a, double b, double C)
	{
 		return Math.Sqrt(a * a + b * b - 2 * a * b * Math.Cos(dtor(C)));
	}
	
	
	/* Returns angle C */
	public double cosLawSolveAngle(double a, double b, double c)
	{
		double temp=(a * a + b * b - c * c) / (2 * a * b);
		if(temp >= -1 && temp <= 1)
			return rtod(Math.Acos(temp));
		return temp;
	}
	
	public double rtod(double i)
	{
		return (180 / Math.PI) * i;
	}
	
	public double dtor(double i)
	{
		return (Math.PI / 180) * i;
	}
}

