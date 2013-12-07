/**
 * Card is a card data type
 * 
 * @author Joseph Lewis 
 * @version August 3, 2009
 */
public class Card
{
    private String title, front, back;
    public int SAVED = 1;
    public int NOT_SAVED = 2;
    public int ERROR = 3;
    
    /**
     * Constructor for objects of class Card
     */
    public Card()
    {
        title = "";
        front = "";
        back = "";
    }
    
    public Card(String tit, String frt, String bak)
    {
        title = tit;
        front = frt;
        back = bak;
    }

    /**
     * Get and set for the private items
     */
    public String getTitle() { return title; }
    public String getFront() { return front; }
    public String getBack()  { return back; }
    
    public void setTitle(String tit) {title = tit;}
    public void setFront(String frt) {front = frt;}
    public void setBack(String bak)  {back = bak;}
    
    /**
     * Save Changes if Nececary
     *
     * @param  title, front, and back
     * 
     */
    public int saveIfNececary(String tit, String frt, String bak)
    {
        int savestate = NOT_SAVED;  //A savestate is returned telling the program if the card needed to be saved or not
        
        if(!tit.equals(title)) //If the new title does not equal the old title
        {
            title = tit;        //Set the old to the new
            savestate = SAVED;  //Update the save state to mean that the card needed saving
        }
        
        if(!frt.equals(front))
        {
            front = frt;
            savestate = SAVED;
        }
        
        if(!bak.equals(back))
        {
            back = bak;
            savestate = SAVED;
        }
        
        return savestate;  //Return the savestate
    }
    
    /**
     * Search Card
     *
     * @param      s, the string to search for
     * @return     A boolean saying if it was found or not
     */
    public boolean searchCard(String s)
    {
        boolean b = false; //If this is not returned true it means the string was not found
        
        s = s.toUpperCase(); //Turn this to upper case so java can Ignore case
        
        if(title.toUpperCase().indexOf(s) != -1) //-1 is returned if the string was not found
        {                                        //If the string was found set b to true
            b = true;
        }
        if(front.toUpperCase().indexOf(s) != -1)
        {
            b = true;
        }
        if(back.toUpperCase().indexOf(s) != -1)
        {
            b = true;
        }
        
        return b;  //True = Found; False = Not Found
    }
}