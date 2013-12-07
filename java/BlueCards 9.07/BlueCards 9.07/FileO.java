
/**
 * FileO Saves your files
 * 
 * @author Joseph Lewis
 * @version August 11, 2009
 */

import java.io.*; //File Writing
import java.util.ArrayList;//For Cards

public class FileO
{
    /**
     * Constructor for objects of class FileO
     */
    public FileO()
    {
    }

    /**
     * Write File - The most important method, writes the file to a destination
     * 
     * @param filePath(String) the path
     */
    public void writeFile(String filePath,ArrayList<Card> cardDeck)
    {
        try
        {
            //If the extention is not .xcrd add it
            if(!filePath.endsWith(".xcrd"))
            {
                //Add an extention to the filePath
                filePath+=".xcrd";
            }
            //Start the file writer then buffer it
            PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(filePath)));
            //Print the Document Definition so Other programs wont mess it up
            printHeadder(out);
            //Print the body(cards)
            printBody(out, cardDeck);
            //Finish Writing
            out.close();
        }
        catch (IOException ex)
        {
            System.err.println("IOException encountered during file output\n"+ex);
        }
    }
    
    /**
     * Print Headder - Prints the document type definition to the top of the document
     * 
     * @param PrintWriter so it prints to the same file with no overwrites
     */
    public void printHeadder(PrintWriter out)
    {
        //The XML Version
        out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
        out.println();
        //The document type definition
        out.write("<!DOCTYPE carddeck [");
        out.println();
        
        out.write("<!ELEMENT carddeck (card*)>");
        out.println();
        out.write("<!ATTLIST carddeck version CDATA #REQUIRED>");
        out.println();
        out.write("<!ELEMENT card (title,front,back)>");
        out.println();
        out.write("<!ELEMENT title (#PCDATA)>");
        out.println();
        out.write("<!ELEMENT front (#PCDATA)>");
        out.println();
        out.write("<!ELEMENT back (#PCDATA)>");
        out.println();
        out.write("]>");
        out.println();
        out.println();
    }
    
    /**
     * Print Body - Prints the body of the XML document
     *
     * @param  cardDeck a list of cards to be printed
     * @param  PrintWriter so it prints to the same file
     */
    public void printBody(PrintWriter out, ArrayList<Card> cardDeck)
    {
        //Output the Root Element
        out.write("<carddeck version=\"1.0\">");
        out.println();
        
        for(int i = 0; i<cardDeck.size(); i++)
        {
            Card c = cardDeck.get(i);
            //Begin the card
            out.write("\t"+"<card>");
            out.println();
            //Output the Title
            out.write("\t\t"+"<title>"+replaceSpecial(c.getTitle())+"</title>");
            out.println();
            //Output the Front
            out.write("\t\t"+"<front>"+replaceSpecial(c.getFront())+"</front>");
            out.println();
            //Output the Back
            out.write("\t\t"+"<back>"+replaceSpecial(c.getBack())+"</back>");
            out.println();
            //End the Card
            out.write("\t"+"</card>");
            out.println();
        }
        
        //Output The End of the Root Element
        out.write("</carddeck>");
        out.println();
    }
    
    /**
     * replaceSpecial replaces tabs and newlines as their
     * xml equivilent
     * @param String
     * @return String
     */
    private String replaceSpecial(String s)
    {
        //Replace LineBreaks
        s = s.replaceAll("\n", "&#X0D;");
        //Replace Tabs
        s = s.replaceAll("\t","&#009;");
        //Replace &lt;  <   less than
        s = s.replaceAll("<", "&lt;");
        //Replace &gt;  >   greater than
        s = s.replaceAll(">", "&gt;");
        //Replace quotes
        s = s.replaceAll("\"", "&quot;");
        //Replace apostrophes
        s = s.replaceAll("\'", "&apos;");
        //Replace & (Done Last to ensure the rest dont get fouled up
        s = s.replaceAll("&", "&amp;");
        return s;   
    }
    
}