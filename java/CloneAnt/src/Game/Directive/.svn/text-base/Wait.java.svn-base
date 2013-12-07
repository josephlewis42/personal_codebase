package Game.Directive;

import Game.Ant;

/**
 * A directive that quite literally does nothing.
 * @author joseph
 *
 */
public class Wait extends Directive
{
	private int waittime;
	
	public Wait(Ant s, int time)
	{
		super(s);
		waittime = time;
	}

	public boolean move()
	{
		waittime--;
		
		return waittime <= 0;
	}
}