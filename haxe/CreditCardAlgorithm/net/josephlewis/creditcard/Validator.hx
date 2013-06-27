package net.josephlewis.creditcard; 

/**
A simple credit card validator that just runs the luhn algorithm against the 
given number. It doesn't even check to see if the string is long enough!
**/
class Validator
{
	/**
		Call this function with a string of digits that represent a credit card
		number.
	**/
	public static function validate(cardNumber : String) : Bool
	{
		return (luhn(cardNumber) == 0);
	}
	
	private static function luhn(numericString : String) : Int
	{
		var output = stringToDigitArray(numericString);
		var sum : Int = 0;
		
		var isEven : Bool = true;
		for( i in output.iterator())
		{
			if(isEven)
			{
				sum += sumOfDigits(i * 2);
			}
			else
			{
				sum += i;
			}
			
			isEven = !isEven; // Invert sign for next iteration
		}
		
		return sum % 10;
	}
	
	private static function stringToDigitArray(numericString : String) : Array<Int>
	{
		var output = new Array<Int>();
		for( i in 0...numericString.length)
		{
			output.push(Std.parseInt(numericString.charAt(i)));
		}
		
		return output;
	}
	
	private static function sumOfDigits(number : Int) : Int
	{
		var sum : Int = 0;
		
		while(number != 0)
		{
			sum += number % Std.int(10);
			number = Std.int(number / Std.int(10));
		}
		
		sum += number;
		
		return sum;
	}
	
	public static function main() : Void
	{
		trace(Validator.validate("1111111111111111"));
		trace(Validator.validate("4271058012370682"));
		trace(Validator.validate("4052047247466840"));
		trace(Validator.validate("4250112315345738"));
		trace(Validator.validate("4302220036446780"));
		trace(Validator.validate("4271382676044056"));
		trace(Validator.validate("4027883785016825"));
		trace(Validator.validate("4125875428334483"));
		trace(Validator.validate("4231380166327600"));
		trace(Validator.validate("4820020713741757"));
		trace(Validator.validate("4013112216053363"));
	}
}
