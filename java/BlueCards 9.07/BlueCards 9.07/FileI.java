/**
 * FileI allows for the reading of xml files
 * 
 * @author Joseph Lewis 
 * @version August 4, 2009
 */

import java.util.ArrayList;     //For Cards
//XML Parsing
import javax.xml.parsers.*;
import org.w3c.dom.*;
import org.xml.sax.*;

public class FileI
{
    // instance variables - replace the example below with your own
    private String fileLocation;

    /**
     * Constructor for objects of class FileI
     */
    public FileI()
    {
    }

    /**
     * ReadFile
     * 
     * @param  fileLocation, the location of the file to be read
     * @return cardList with new cards 
     */
    public ArrayList<Card> readFile(String fileLocation)
    {
        //Variables
        ArrayList<Card> cardList = new ArrayList<Card>();
        return readFile(fileLocation, cardList);
    }
    
    /**
     * ReadFile
     * 
     * @param fileLocation, the location of the file to be read
     * @param cardList, the array of cards to add to
     * @return cardList with new cards
     */
    public ArrayList<Card> readFile(String fileLocation, ArrayList<Card> cardList)
    {
        Document xmlDoc;
        double version;
        
        xmlDoc = getXMLDocument(fileLocation);
        if(xmlDoc != null)
        {
            version = getVersion(xmlDoc);
            System.out.println(version);
            if(version <= 1.0)
            {
                cardList = createList(xmlDoc,cardList);
            }
        }
        
        return cardList;
    }
    
    /**
     * getXMLDocument - reads an xml document into a list of cards
     * 
     * @param fileLocaton, the location of the file to read
     * @return an XML Document
     */
    private static Document getXMLDocument(String fileLoc)
    {
        //Prevent a file url exception
        fileLoc = "file:///"+fileLoc;
        try
        {
            DocumentBuilderFactory factory =
                DocumentBuilderFactory.newInstance();
            factory.setIgnoringComments(true);
            factory.setIgnoringElementContentWhitespace(true);
            factory.setValidating(true);
            DocumentBuilder builder = factory.newDocumentBuilder();
            return builder.parse(new InputSource(fileLoc));
        }
        catch (Exception e)
        {
            Dialogs d = new Dialogs();
            d.showInformationDialog("Title","Error                                                         \n"+e);
        }
        return null;
    }
       
    /**
     * getVersion - Reads a version from the root element of an xml file
     * 
     * @param Document, an xml file to read
     * @return a double version
     */
    private double getVersion(Document doc)
    {
        Element root = doc.getDocumentElement();

        String versionstr = root.getAttribute("version");
        double versiondbl = Double.parseDouble(versionstr);
        
        return versiondbl;
    }
    
    /**
     * createList - Creates an array list with all of the card itmes needed
     * 
     * @param doc, an xml document
     * @return ArrayList<Card>
     */
    private ArrayList<Card> createList(Document doc, ArrayList<Card> cardList)
    {
        Element root = doc.getDocumentElement();
        
        Element cardElement = (Element)root.getFirstChild();
        
        while (cardElement != null)
        {
            Card c = getCardFromElement(cardElement);
            cardList.add(c);
            
            cardElement = (Element)cardElement.getNextSibling();
        }
        return cardList;
    }
    
    /**
     * getCardFromElement - this will get information from the cardElement and will
     * set it to an actual card
     * 
     * According to the XML  Document Type Definition (DTD)
     * A card is structured:
     * Title
     * Front
     * Back
     * 
     * @param Element, an xml element with 
     * @return Card
     */
    private Card getCardFromElement (Element e)
    {
        e = (Element)e.getFirstChild();
        //Get the Title Element
        Element tElement = (Element)e;
        String title = getTextValue(tElement).trim();
        System.out.println(title);

        //Get the Front Element
        Element fElement = (Element)e.getNextSibling();
        String front = getTextValue(fElement).trim();

        //Get the Back Element
        Element bElement = (Element)fElement.getNextSibling();
        String back = getTextValue(bElement).trim();

        //Replace all Special Characters This is auto done in java
        //title = replaceSpecial(title);
        //front = replaceSpecial(front);
        //back = replaceSpecial(back);
        
        //Create Card
        Card c = new Card(title,front,back);
        //Return Card
        return c;
    }
    
    /**
     * getTextValue - Gets the text value of an element
     * @param Node
     * @return String
     */
    private String getTextValue(Node n)
    {
        return n.getFirstChild().getNodeValue();
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
        s = s.replaceAll("&#X0D;", "\n");
        //Replace Tabs
        s = s.replaceAll("&#009;", "\t");
        //Replace &lt;  <   less than
        s = s.replaceAll("&lt;", "<");
        //Replace &gt;  >   greater than
        s = s.replaceAll("&gt;", ">");
        //Replace quotes
        s = s.replaceAll("&quot;","\"");
        //Replace apostrophes
        s = s.replaceAll("&apos;","\'");
        //Replace & (Done Last to ensure the rest dont get fouled up
        s = s.replaceAll("&amp;", "&");
        return s;   
    }
}