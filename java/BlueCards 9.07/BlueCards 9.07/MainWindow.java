/**
 * Main Window is the user interface of BlueCards
 * 
 * @author Joseph Lewis 
 * @version August 12,2009
 */

//Layout Managers
import java.awt.BorderLayout;       //Used for most of the panels
import java.awt.CardLayout;         //Used for "Flipping" Panels from one to another in the JFrame
import java.awt.GridLayout;         //Used for the layout of some items on a grid

//Event Handlers
import java.awt.event.ActionListener;       //Used to listen for Actions Performed on Swing Items
import java.awt.event.MouseListener;        //Used to listen for What the mouse is doing
import java.awt.event.FocusListener;        //Used to listen for What swing item is currently selected
import java.awt.event.WindowListener;       //Used to listen for What is happening to the JFrame

//Event Adapters
import java.awt.event.WindowAdapter;    //Used to change the window

//Events
import java.awt.event.ActionEvent;  //The event given when An action is performed
import java.awt.event.MouseEvent;   //The event given when The mouse clicks
import java.awt.event.FocusEvent;   //The event given when A JItem gains or loses focus
import java.awt.event.WindowEvent;  //The event given when The Window Changes
import java.awt.event.KeyEvent;     //The event given when A Key Is Pressed

//Exceptions
import java.io.IOException;         //Used when IO is not properly working only for the ClipBoard in this class

//Java Swing Components
import javax.swing.*;   //The user interface

//ClipBoard
import java.awt.Toolkit;
import java.awt.datatransfer.*;

//DataTypes
import java.util.ArrayList;     //For Cards

//Data Manipulation
import java.lang.StringBuilder; //For working with text

//JList Rendering
import java.awt.Component;
import java.awt.Color;
import java.awt.SystemColor;





public class MainWindow extends JFrame implements ActionListener, MouseListener, FocusListener
{
    //Constants
    private static String HOMEPANEL   = "Home Panel";   //Used when asking the panelDeck for a panel
    private static String SEARCHPANEL = "Search Panel"; //Used when asking the panelDeck for a panel
    private static String CARDPANEL   = "Card Panel";   //Used when asking the panelDeck for a panel
    
    //Used For Event Validation
    private boolean bTitleFieldFocoused = false;    //Used to determine if the carat is in the title field
    private boolean bFrontAreaFocoused  = false;    //Used to determine if the carat is in the Front area
    private boolean bBackAreaFocoused   = false;    //Used to determine if the carat is in the Back area
	private boolean bSearchFieldFocoused = false; 	//Used to determine if the carat is in the Search Area

    //Document Variables
    private String      currentFilePath = "";    //Determines where the file is to be saved
    private boolean     docNotSaved     = false; //Used to determine if the document is NOT saved
    private String[]    fileFilter      = { "Card Deck XML Files", "xcrd"}; //Used for the file dialogs
    private int         currentCard     = 0;    //Used to determine which card is being edited
	private String		searchString 	= "";	//Used to store the string that is searched for
    
    //Card Information
    private ArrayList<Card> cardDeck = new ArrayList<Card>();   //Used for storing all of the cards
    private String[] gsCardTitles;                              //The array of titles of the cards used for JLists
    
    //Graphical User Interface Items
    private JPanel      panelDeck = new JPanel();    //Holds all of the other panels that can be "flipped" to
    private JMenuItem   deckNew,deckOpen,deckSave,deckSaveAs,deckImport,deckQuit;   //The deck menu buttons
    private JMenuItem   cardCut,cardCopy,cardPaste,cardNew,cardDeleteMenu;  //The card menu buttons
    private JMenuItem   helpHelp,helpAbout;                                 //The help menu buttons
    private JButton     homeButton, cardButton, findButton;                 //The major 3 always there
    private JButton     deleteMultipleButton, openButton;                   //For Home toolbar
    private JButton     newButton;                                          //For H&C Toolbars
    private JButton     backButton, nextButton, deleteSingleButton;         //For Card Toolbar
	private JButton		searchButton;										//For Search Toolbar
    private JList       mainList, searchList;                               //Displays cards using gsCardTitles
    private JTextArea   frontArea,backArea;                                 //For editing front and back of cards
    private JTextField  titleField, searchField;                            //For editing titles of cards and searching
    
    //Other Class Constructors
    private CardLayout cardLayout;      //Allow for card layout
    private Dialogs d = new Dialogs();  //Allow easy dialog creation
    private FileI fin = new FileI();    //The document parsing class
    private ClassLoader classLoader = this.getClass().getClassLoader();     //Gets files inside of the jar


    /**
     * Constructor 1 (No Filepath)
     * 
     * Call the other constructor
     */
    public MainWindow()
    {
        this(null);
    }
    
    /**
     * Constructor 2 (Filepath)
     * 
     * If null is the filepath then create a new document
     * If there is a filepath then create a document through that
     */
    public MainWindow(String fileLocation)
    {
        //Set Variables
        currentFilePath = fileLocation;
        
        
        //Set up deck
        if(fileLocation == null)
        {
            //Set up a new card deck with a semi tutorial card
            cardDeck = new ArrayList<Card>();
            cardDeck.add(0,new Card("Double Click Me For Help","Find the tutorials in the help menu under help","Delete this card by pressing delete above."));
            
            //Set the file directory to "" to avoid errors in the future
            currentFilePath = "";
        }
        else
        {
            //Have the XML Reader read the file into the ArrayList<Card> cardDeck
            cardDeck = fin.readFile(fileLocation);
        }
        
        //Draw the main window on screen
        drawGUI();
        
        
    }
    
    /**
     * DrawGui starts the Graphical User Interface
     */
    public void drawGUI()
    {
        //Create a new "Deck" so frames can be changed during the program operation
        panelDeck = new JPanel(new CardLayout());
        //For now just add the home frame
        //Later actions will be called when the user wants to switch
        panelDeck.add(drawHomePanel(), HOMEPANEL);
        
        //Add the panelDeck
        this.add(panelDeck);
        
        //Set the standard program menubar
        this.setJMenuBar(drawMenuBar());
        
        //Window Options
        this.setIconImage(new ImageIcon(classLoader.getResource("icons/tb_card.png")).getImage()); //Set the image icon
        this.setDefaultCloseOperation( JFrame.DO_NOTHING_ON_CLOSE); //Dont do anything, a listener will do this
        this.setTitle("Blue Cards"); //Set the title the user will see
        this.setSize(700,600);  //700 px by 600px
        this.setLocationRelativeTo (null); //Set in center of screen
        this.setResizable(true); //The user can resize the window
        this.setVisible(true);  //This window is visible.
        
        //Do this so a do you want to save before quitting message can be shown
        //if it is neccecary
        //If someone tries to quit do the onQuitAction() method
        WindowListener wndCloser = new WindowAdapter() {
             public void windowClosing(WindowEvent e) {
                 onQuitAction();
                }
            };
            addWindowListener(wndCloser);
    } 
    
    /**
     * Draw Home Panel - Draws the main Panel for the user
     * @return     JPanel
     */
    private JPanel drawHomePanel()
    {
        //Create the panel and give it a simple border layout
        JPanel homePanel = new JPanel(new BorderLayout());
        //Add the toolbar
        homePanel.add(drawHomeToolBar(),BorderLayout.NORTH);
        //Add the list
        mainList = new JList(getAllCardsArray(cardDeck));
        //Color the cells according to the system theme
        mainList.setCellRenderer(new CellRenderer());
        //Hilight the currently selected card
        mainList.setSelectedIndex(currentCard);
        //Add a mouse listener that if there is a double click on an item opens the item
        mainList.addMouseListener(this);
        //Add a scrollbar because java wont do this
        JScrollPane scroller = new JScrollPane(mainList, 
                                                JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, 
                                                JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
        
        //Add the scroller to the panel because the scroller contains the list
        homePanel.add(scroller,BorderLayout.CENTER);
        
        return homePanel;
    }
    
    /**
     * drawCardPanel - Draws the frame for editing cards
     *
     * @param  int CardIndex (the card that is being edited)
     * @param  int = -1 if this is true make a new card
     * @return JPanel
     */
    public JPanel drawCardPanel(int selectedCard)
    {
        //If the card is a new one this information will stay
        String cardTitle = "*Untitled*";
        String cardFront = "";
        String cardBack = "";
        
        //Do the below if the card is an existing one
        if(selectedCard != -1)
        {
            //Update the current card number
            currentCard = selectedCard;
            //Get the information from the selected card
            cardTitle = cardDeck.get(selectedCard).getTitle();
            cardFront = cardDeck.get(selectedCard).getFront();
            cardBack = cardDeck.get(selectedCard).getBack();
        }
        else
        {
            //Create a new card with the above variables
            Card newCard = new Card(cardTitle,cardFront,cardBack);
            //Add this new card to the deck
            cardDeck.add(0, newCard);
            //Set it as selected
            selectedCard = 0;
            //Update the current card to be the selected card
            currentCard = selectedCard;
        }
        
        //Create the JPanel that will hold the toolbar and input bars
        JPanel cardPanel = new JPanel(new BorderLayout());
        //Add the toolbar for this particular panel
        cardPanel.add(drawCardToolBar(),BorderLayout.NORTH);
            //This panel will go inside the cardPanel, allowing the toolbar 
            //to pe placed anywhere (on the above panel N,S,E,W) without disturbing
            //the other components
            JPanel innerPanel = new JPanel(new BorderLayout());
                //Create the panel for the title text field and label
                JPanel iPNorth = new JPanel(new GridLayout(0,1));//Arrange components on a Y Axis only
                
                //Create a label so the user knows what the box is for
                JLabel titleLabel = new JLabel("Title:");
                //Add It
                iPNorth.add(titleLabel);
        
                //Create a text box for the user to enter the title
                titleField = new JTextField(cardTitle);
                titleField.addMouseListener(this);
                titleField.addFocusListener(this);
                //Add it
                iPNorth.add(titleField);
                
            innerPanel.add(iPNorth, BorderLayout.NORTH);
            
                //Create a text area for the front of the card
                frontArea = new JTextArea(cardFront);
                frontArea.setLineWrap(true); //Wrap characters so they dont go off screen
                frontArea.addMouseListener(this);
                frontArea.addFocusListener(this);
                JScrollPane frontScroller = new JScrollPane(frontArea);//Add a scrollbar
                //Create a text area for the back of the card
                backArea = new JTextArea(cardBack);
                JScrollPane backScroller = new JScrollPane(backArea);
                backArea.addMouseListener(this);
                backArea.addFocusListener(this);
                //Add both things to a user sizable split pane so the user can move it
                JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT,frontScroller,backScroller);
                //Set the divider in the center width/2
                split.setDividerLocation(200);
            innerPanel.add(split, BorderLayout.CENTER);
        cardPanel.add(innerPanel,BorderLayout.CENTER);
        return cardPanel;
    }
    
    /**
     * Draw Search Panel - Draws the Search Panel for the user
     * @return     JPanel
     */
    private JPanel drawSearchPanel()
    {
        //Create the panel and give it a simple border layout
        JPanel searchPanel = new JPanel(new BorderLayout());
        //Add the toolbar
        searchPanel.add(drawSearchToolBar(),BorderLayout.NORTH);
        //Add the list
        searchList = new JList(getSearchCardsArray(cardDeck, searchString));
        //Color the cells according to the system theme
        mainList.setCellRenderer(new CellRenderer());
        //Hilight the currently selected card
        searchList.setSelectedIndex(currentCard);
        //Add a mouse listener that if there is a double click on an item opens the item
        searchList.addMouseListener(this);
        //Add a scrollbar because java wont do this
        JScrollPane scroller = new JScrollPane(searchList, 
                                                JScrollPane.VERTICAL_SCROLLBAR_ALWAYS, 
                                                JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
        
        //Add the scroller to the panel because the scroller contains the list
        searchPanel.add(scroller,BorderLayout.CENTER);
        
        return searchPanel;
    }
    
    
    
    /**
     * getAllCardsArray
     * @param ArrayList<card>
     * @return [] string (The titles of each card)
     */
    private String[] getAllCardsArray(ArrayList<Card> arrayListInput)
    {
        //Create a string with the number of elements as the arrayList
        String[] titles = new String[arrayListInput.size()];
        
        for(int i = 0; i<titles.length; i++)
        {
            titles[i] = arrayListInput.get(i).getTitle();
        }
        
        return titles;
    }
    
    /**
     * getSearchCardsArray - Get the array for the search
     * @param ArrayList<card>
     * @param Search The String To Search For
     * @return [] string (The titles of each card)
     */
    private String[] getSearchCardsArray(ArrayList<Card> arrayListInput, String search)
    {
        //Create a string with the number of elements as the arrayList
        String[] titles = new String[arrayListInput.size()];
        ArrayList<String> searchList = new ArrayList<String>();
        
        for(int i = 0; i<titles.length; i++)
        {
            if(arrayListInput.get(i).searchCard(search))//Returns True if the string is found in the card
            {
                String s = arrayListInput.get(i).getTitle();
                s += ", Card # "+i;
                searchList.add(s);
            }
        }
        
        for(int i = 0; i<searchList.size(); i++)
        {
            titles[i] = searchList.get(i);
        }
        
        return titles;
    }
    
    /**
     * drawHomeToolbar - Draws the Home Tool Bar
     * @return JToolBar
     */
    private JToolBar drawHomeToolBar()
    {
        JToolBar tb = new JToolBar();
        
        //Create the first three buttons to select the current 
        //frame
        ImageIcon iconHouse = new ImageIcon(classLoader.getResource("icons/tb_house.png"));
        homeButton = new JButton("Home",iconHouse);
        homeButton.setEnabled(false);
        tb.add(homeButton);
        homeButton.addActionListener(this);
        //Card
        ImageIcon iconCard = new ImageIcon(classLoader.getResource("icons/tb_card.png"));
        cardButton = new JButton("Card",iconCard);
        tb.add(cardButton);
        cardButton.addActionListener(this);
        //Search
        ImageIcon iconFind = new ImageIcon(classLoader.getResource("icons/tb_find.png"));
        findButton = new JButton("Find",iconFind);
        tb.add(findButton);
        findButton.addActionListener(this);
        //Add the seperator for the different buttons
        tb.addSeparator();
        //New
        ImageIcon iconNew = new ImageIcon(classLoader.getResource("icons/tb_new.png"));
        newButton = new JButton("New",iconNew);
        tb.add(newButton);
        newButton.addActionListener(this);
        //Open
        ImageIcon iconOpen = new ImageIcon(classLoader.getResource("icons/tb_edit.png"));
        openButton = new JButton("Open",iconOpen);
        tb.add(openButton);
        openButton.addActionListener(this);
        //Delete
        ImageIcon iconDelete = new ImageIcon(classLoader.getResource("icons/tb_delete.png"));
        deleteMultipleButton = new JButton("Delete",iconDelete);
        tb.add(deleteMultipleButton);
        deleteMultipleButton.addActionListener(this);
        
        return tb;
    }
    
    /**
     * drawCardToolBar - Draws the Card Tool Bar
     * @return JToolBar
     */
    private JToolBar drawCardToolBar()
    {
        JToolBar tb = new JToolBar();
        
        //Create the first three buttons to select the current 
        //frame
        ImageIcon iconHouse = new ImageIcon(classLoader.getResource("icons/tb_house.png"));
        homeButton = new JButton("Home",iconHouse);
        tb.add(homeButton);
        homeButton.addActionListener(this);
        //Card
        ImageIcon iconCard = new ImageIcon(classLoader.getResource("icons/tb_card.png"));
        cardButton = new JButton("Card",iconCard);
        cardButton.setEnabled(false);
        tb.add(cardButton);
        //Search
        ImageIcon iconFind = new ImageIcon(classLoader.getResource("icons/tb_find.png"));
        findButton = new JButton("Find",iconFind);
        tb.add(findButton);
        findButton.addActionListener(this);
        //Add the seperator for the different buttons
        tb.addSeparator();
        //Navigation buttons go here (back, foreword)

        //Back
        ImageIcon iconBack = new ImageIcon(classLoader.getResource("icons/tb_prev.png"));
        backButton = new JButton(iconBack);
        if(currentCard == 0)
        {
            backButton.setEnabled(false);
        }
        tb.add(backButton);
        backButton.addActionListener(this);
        
        //Foreword
        ImageIcon iconNext = new ImageIcon(classLoader.getResource("icons/tb_next.png"));
        nextButton = new JButton(iconNext);
        if(currentCard == cardDeck.size()-1)
        {
            nextButton.setEnabled(false);
        }
        tb.add(nextButton);
        nextButton.addActionListener(this);
        
        //Add the seperator for the card edit buttons
        tb.addSeparator();
        //New
        ImageIcon iconNew = new ImageIcon(classLoader.getResource("icons/tb_new.png"));
        newButton = new JButton("New",iconNew);
        tb.add(newButton);
        newButton.addActionListener(this);
        //Delete
        ImageIcon iconDelete = new ImageIcon(classLoader.getResource("icons/tb_delete.png"));
        deleteSingleButton = new JButton("Delete",iconDelete);
        tb.add(deleteSingleButton);
        deleteSingleButton.addActionListener(this);
        
        return tb;
    }
    
	/**
     * drawSearchToolbar - Draws the Search Tool Bar
     * @return JToolBar
     */
    private JToolBar drawSearchToolBar()
    {
        JToolBar tb = new JToolBar();
        
        //Create the first three buttons to select the current 
        //frame
        ImageIcon iconHouse = new ImageIcon(classLoader.getResource("icons/tb_house.png"));
        homeButton = new JButton("Home",iconHouse);
        tb.add(homeButton);
        homeButton.addActionListener(this);
        //Card
        ImageIcon iconCard = new ImageIcon(classLoader.getResource("icons/tb_card.png"));
        cardButton = new JButton("Card",iconCard);
        tb.add(cardButton);
        cardButton.addActionListener(this);
        //Search
        ImageIcon iconFind = new ImageIcon(classLoader.getResource("icons/tb_find.png"));
        findButton = new JButton("Find",iconFind);
        tb.add(findButton);
		findButton.setEnabled(false);
        //Add the seperator for the different buttons
        tb.addSeparator();
        
		searchString = (searchString.equals("")) ? "Type Here To Search..." : searchString;

		searchField = new JTextField(searchString);
		searchField.addFocusListener(this);
		tb.add(searchField);
        //Delete
        searchButton = new JButton("Press to Search");
        tb.add(searchButton);
        searchButton.addActionListener(this);
        
        return tb;
    }


    /**
     * drawMenuBar
     * Draws the main menu system for the user
     * @return     JFrame
     */
    private JMenuBar drawMenuBar()
    {
        //Get the class loader so images in the jar can be
        //accessed
        ClassLoader cl = this.getClass().getClassLoader();
        //Create the MenuBar for the program
        JMenuBar mb = new JMenuBar();
            JMenu deckMenu = new JMenu("Deck");//Create The Deck Menu
            JMenu cardMenu = new JMenu("Card");//Create the Card menu
            JMenu helpMenu = new JMenu("Help");//Create the help menu
        
                //Create the menu items for each
                    //Deck
                        //New
                            //LookAndFeel
                            ImageIcon iconNew = new ImageIcon(cl.getResource("icons/file_new.png"));
                            deckNew = new JMenuItem("New",iconNew);
                            deckNew.setToolTipText("Create A New Document");
                            //Actions
                            deckNew.addActionListener(this);
                            deckNew.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_N, ActionEvent.CTRL_MASK));
                            //Add
                            deckMenu.add(deckNew);
                        //Open
                            //LookAndFeel
                            ImageIcon iconOpen = new ImageIcon(cl.getResource("icons/file_open.png"));
                            deckOpen = new JMenuItem("Open",iconOpen);
                            deckOpen.setToolTipText("Open An Existing Document");
                            //Actions
                            deckOpen.addActionListener(this);
                            deckOpen.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_O, ActionEvent.CTRL_MASK));
                            //Add
                            deckMenu.add(deckOpen);
                        //Save
                            //LookAndFeel
                            ImageIcon iconSave = new ImageIcon(cl.getResource("icons/file_save.png"));
                            deckSave = new JMenuItem("Save",iconSave);
                            deckSave.setToolTipText("Save the Document");
                            //Actions
                            deckSave.addActionListener(this);
                            deckSave.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_S, ActionEvent.CTRL_MASK));
                            //Add
                            deckMenu.add(deckSave);
                        //SaveAs
                            //LookAndFeel
                            deckSaveAs = new JMenuItem("SaveAs");
                            deckSaveAs.setToolTipText("Save the document under another name");
                            //Actions
                            deckSaveAs.addActionListener(this);
                            //Add
                            deckMenu.add(deckSaveAs);
                        //-----
                            deckMenu.addSeparator();
                        //Import
                            //LookAndFeel
                            deckImport = new JMenuItem("Import");
                            deckImport.setToolTipText("Import Cards From Another Document");
                            //Actions
                            deckImport.addActionListener(this);
                            //Add
                            deckMenu.add(deckImport);
                        //-----
                            deckMenu.addSeparator();
                        //Quit
                            //LookAndFeel
                            ImageIcon iconQuit = new ImageIcon(cl.getResource("icons/file_quit.png"));
                            deckQuit = new JMenuItem("Quit",iconQuit);
                            deckQuit.setToolTipText("Quit The Program");
                            //Actions
                            deckQuit.addActionListener(this);
                            deckQuit.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_Q, ActionEvent.CTRL_MASK));
                            //Add
                            deckMenu.add(deckQuit);
                    //Card
                        //Cut
                            //LookAndFeel
                            ImageIcon iconCut = new ImageIcon(cl.getResource("icons/edit_cut.png"));
                            cardCut = new JMenuItem("Cut",iconCut);
                            //Actions
                            cardCut.addActionListener(this);
                            cardCut.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_X, ActionEvent.CTRL_MASK));
                            //Add
                            cardMenu.add(cardCut);
                        //Copy
                            //LookAndFeel
                            ImageIcon iconCopy = new ImageIcon(cl.getResource("icons/edit_copy.png"));
                            cardCopy = new JMenuItem("Copy",iconCopy);
                            //Actions
                            cardCopy.addActionListener(this);
                            cardCopy.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_C, ActionEvent.CTRL_MASK));
                            //Add
                            cardMenu.add(cardCopy);
                        //Paste
                            //LookAndFeel
                            ImageIcon iconPaste = new ImageIcon(cl.getResource("icons/edit_paste.png"));
                            cardPaste = new JMenuItem("Paste",iconPaste);
                            //Actions
                            cardPaste.addActionListener(this);
                            cardPaste.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_V, ActionEvent.CTRL_MASK));
                            //Add
                            cardMenu.add(cardPaste);
                        //-----
                            cardMenu.addSeparator();
                        //New
                            //LookAndFeel
                            cardNew = new JMenuItem("New",iconNew);//IconNew is allready defined no need to do it again
                            //Actions
                            cardNew.addActionListener(this);
                            cardNew.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_N, ActionEvent.SHIFT_MASK));
                            //Add
                            cardMenu.add(cardNew);
                    //Help
                        //Help
                            //LookAndFeel
                            ImageIcon iconHelp = new ImageIcon(cl.getResource("icons/help_help.png"));
                            helpHelp = new JMenuItem("Help",iconHelp);
                            //Actions
                            helpHelp.addActionListener(this);
                            helpHelp.setAccelerator(KeyStroke.getKeyStroke("F1"));
                            //Add
                            helpMenu.add(helpHelp);
                        //About
                            //LookAndFeel
                            ImageIcon iconAbout = new ImageIcon(cl.getResource("icons/help_about.png"));
                            helpAbout = new JMenuItem("About",iconAbout);
                            //Actions
                            helpAbout.addActionListener(this);
                            //Add
                            helpMenu.add(helpAbout);
        
        mb.add(deckMenu);
        mb.add(cardMenu);
        mb.add(helpMenu);
        
        return mb;
    }
    
    
    /**
     * actionPerformed allows listeners to be useful
     */
    public void actionPerformed(ActionEvent e)
    {
        //Before any action is done try to save any open card
        try{
             saveOpenCard();
            }catch(Exception ex){}
        //Create actions for the main menubar

		if(e.getSource() == searchButton)
        {
            searchString = searchField.getText();

			searchCards();
        }

        if(e.getSource() == deckQuit)
        {
            onQuitAction();
        }
        
        if(e.getSource() == deckNew)
        {
            MainWindow w = new MainWindow();
        }
        
        if(e.getSource() == deckOpen)
        {
            String loc = d.showOpenDialog(fileFilter, "", false, true, false);
            MainWindow w = new MainWindow(loc);
        }
        
        if(e.getSource() == deckSave)
        {
            saveCards(currentFilePath);
        }
        
        if(e.getSource() == deckSaveAs)
        {
            saveCards("");
        }
        
        if(e.getSource() == deckImport)
        {
            importCards();
        }
        
        if(e.getSource() == cardCut)
        {
            SwingUtilities.invokeLater( new Runnable()
            {
                public void run()
                {
                    cutText();
                }
            });
        }
        
        if(e.getSource() == cardCopy)
        {
            copyText();
        }
        
        if(e.getSource() == cardPaste)
        {
            SwingUtilities.invokeLater( new Runnable()
            {
                public void run()
                {
                    pasteText();
                }
            });
        }
        
        if(e.getSource() == cardNew)
        {
            newCard();
        }
        
        if(e.getSource() == helpHelp)
        {
            d.showInformationDialog("Information","Not Yet Implimented");
        }
        
        if(e.getSource() == helpAbout)
        {
            d.showInformationDialog("About Blue Cards","<html><b>Version:</b> 9.08\n"+
                                                        "<html><b>Created By:</b> Joseph Lewis\n"+
                                                        "<html><b>Created For:</b> The BlueOffice Project\n"+
                                                        "<html><a href=\"http:BlueWriter.sourceforge.net\">http://BlueWriter.sourceforge.net</a>\n"+
                                                        "<html><b>Icons By:</b>Mark James (famfamfam.com)");
        }
        //Create actions for all the toolbars
        
        if(e.getSource() == homeButton)
        {
            drawHome();
        }
        if(e.getSource() == cardButton)
        {
            openCard(currentCard);
        }
        if(e.getSource() == findButton)
        {
            searchCards();
        }
        
        //Create actions for the home toolbar (newButton, deleteButton, openButton)
        if(e.getSource() == newButton)
        {
            newCard();
            
        }
        if(e.getSource() == deleteSingleButton)
        {
            deleteCard();
        }
        if(e.getSource() == deleteMultipleButton)
        {
            deleteCards();
        }
        
        if(e.getSource() == openButton)
        {
            openCard(mainList.getSelectedIndex());
        }
        //Create actions for the card toolbar(back, foreword)
        if(e.getSource() == backButton)
        {
            currentCard--;
            openCard(currentCard);
        }
        if(e.getSource() == nextButton)
        {
            currentCard++;
            openCard(currentCard);
        }
    }
    
    
    /**
     * Mouse Listener - allows mouse events to be useful
     *
     * @param  event
     */
    public void mousePressed(MouseEvent e) {}
    public void mouseReleased(MouseEvent e) {}
    public void mouseEntered(MouseEvent e) {}
    public void mouseExited(MouseEvent e) {}
    public void mouseClicked(MouseEvent e) 
    {
        //Its a whole lot less work for the computer 
        //if the click is just single to skip all this
        if (e.getClickCount() == 2)
        {
            if(e.getSource() == mainList)
            {
                openCard(mainList.getSelectedIndex());
            }

			if(e.getSource() == searchList)
            {
				//Create A String Builder To Help Find The Card Location
				StringBuilder sb = new StringBuilder((String)searchList.getSelectedValue());
				//Have it get the last time a pound sign and space are in the text
                int i = sb.lastIndexOf("#");
				//Cut the number off the end using the index of # to find the exact location of the number
				i+=2; //Movepast the pound and space
				String s = sb.substring(i);//Get the number
				i = Integer.parseInt(s);
				//Open the selected card from the number on the end
                openCard(i);
            }
        }
        
        //Check if it was a right click if so
        if (e.getButton() == MouseEvent.BUTTON3)
        {
            if(e.getSource() != mainList  && e.getSource() != searchList)
            {
                showCardPopup(e);
            }
        }
    }

    /**
     * Focous Listener, remembers which text item had the focus
     */
    public void focusGained(FocusEvent e) 
    {
        //Set all focous to false except the one that called the focous event
        bTitleFieldFocoused = false;
        bFrontAreaFocoused 	= false;
        bBackAreaFocoused 	= false;
		bSearchFieldFocoused = false;
        //Set the one to true
        if(e.getSource() == titleField)
        {
            bTitleFieldFocoused = true;
        }
        
        if(e.getSource() == frontArea)
        {
            bFrontAreaFocoused = true;
        }
        
        if(e.getSource() == backArea)
        {
            bBackAreaFocoused = true;
        }
    
		if(e.getSource() == searchField)
        {
            bSearchFieldFocoused = true;
        }
    }

    public void focusLost(FocusEvent e) {}

    
    
    
    /**
     *        ////////////////////////////////
     *       //////Actions Go Below Here/////
     *      ////////////////////////////////
     */
    
    /**
     * Cut - Cut text From Cards
     *
     * @param  e - A window Event
     */
    public void cutText()
    {
        StringBuilder sb = new StringBuilder();
        if(bFrontAreaFocoused)
        {
            //Get the start and end of the user's selection (what is hilighted in the text area)
            int st = frontArea.getSelectionStart();
            int end = frontArea.getSelectionEnd();
            //Start a stringBuilder so we can work on the text 
            sb = new StringBuilder(frontArea.getText());
            //Seperate only the hilighted stuff
            String cutText = sb.substring(st,end);
            //Send it to the system clipboard
            setClipboard(cutText);
            
            //Remove the string from the area
            sb.delete(st,end);
            frontArea.setText(sb.toString());
        }
        
        if(bBackAreaFocoused)
        {
            //Get the start and end of the user's selection (what is hilighted in the text area)
            int st = backArea.getSelectionStart();
            int end = backArea.getSelectionEnd();
            //Start a stringBuilder so we can work on the text 
            sb = new StringBuilder(backArea.getText());
            //Seperate only the hilighted stuff
            String cutText = sb.substring(st,end);
            //Send it to the system clipboard
            setClipboard(cutText);
            
            //Remove the string from the area
            sb.delete(st,end);
            backArea.setText(sb.toString());
        }

        if(bTitleFieldFocoused)
        {
            //Get the start and end of the user's selection (what is hilighted in the text area)
            int st = titleField.getSelectionStart();
            int end = titleField.getSelectionEnd();
            //Start a stringBuilder so we can work on the text 
            sb = new StringBuilder(titleField.getText());
            //Seperate only the hilighted stuff
            String cutText = sb.substring(st,end);
            //Send it to the system clipboard
            setClipboard(cutText);
            
            //Remove the string from the area
            sb.delete(st,end);
            titleField.setText(sb.toString());   
        }

		if(bSearchFieldFocoused)
        {
            //Get the start and end of the user's selection (what is hilighted in the text area)
            int st = searchField.getSelectionStart();
            int end = searchField.getSelectionEnd();
            //Start a stringBuilder so we can work on the text 
            sb = new StringBuilder(searchField.getText());
            //Seperate only the hilighted stuff
            String cutText = sb.substring(st,end);
            //Send it to the system clipboard
            setClipboard(cutText);
            
            //Remove the string from the area
            sb.delete(st,end);
            searchField.setText(sb.toString());   
        }
        
        //repaint all of the text areas so the text appears.
        frontArea.repaint();
        backArea.repaint();
        titleField.repaint();
		searchField.repaint();
        this.repaint();
    }
    
    
    /**
     * Copy - Copy Text From Cards
     *
     * @param  e - A window Event
     */
    public void copyText()
    {
        StringBuilder sb = new StringBuilder();
        
        if(bFrontAreaFocoused)
        {
            //Get the start and end of the user's selection (what is hilighted in the text area)
            int st = frontArea.getSelectionStart();
            int end = frontArea.getSelectionEnd();
            //Start a stringBuilder so we can work on the text 
            sb = new StringBuilder(frontArea.getText());
            //Seperate only the hilighted stuff
            String copiedText = sb.substring(st,end);
            //Send it to the system clipboard
            setClipboard(copiedText);
        }
        
        if(bBackAreaFocoused)
        {
            //Get the start and end of the user's selection (what is hilighted in the text area)
            int st = backArea.getSelectionStart();
            int end = backArea.getSelectionEnd();
            //Start a stringBuilder so we can work on the text 
            sb = new StringBuilder(backArea.getText());
            //Seperate only the hilighted stuff
            String copiedText = sb.substring(st,end);
            //Send it to the system clipboard
            setClipboard(copiedText);
        }

        if(bTitleFieldFocoused)
        {
            //Get the start and end of the user's selection (what is hilighted in the text area)
            int st = titleField.getSelectionStart();
            int end = titleField.getSelectionEnd();
            //Start a stringBuilder so we can work on the text 
            sb = new StringBuilder(titleField.getText());
            //Seperate only the hilighted stuff
            String copiedText = sb.substring(st,end);
            //Send it to the system clipboard
            setClipboard(copiedText);
        }
    }
    
    /**
     * Paste - Paste Text To Cards
     *
     * @param  e - A window Event
     */
    public void pasteText()
    {
        
        StringBuilder sb = new StringBuilder();
        if(bFrontAreaFocoused)
        {
            //Get the start and end of the user's selection (what is hilighted in the text area)
            int st = frontArea.getSelectionStart();
            int end = frontArea.getSelectionEnd();
            //Start a stringBuilder so we can work on the text 
            sb = new StringBuilder(frontArea.getText());
            //Get text from the system clipboard
            String pasteText = getClipboard();
            
            //Replace the string
            sb.replace(st,end,pasteText);
            frontArea.setText(sb.toString());
        }
        
        if(bBackAreaFocoused)
        {
            //Get the start and end of the user's selection (what is hilighted in the text area)
            int st = backArea.getSelectionStart();
            int end = backArea.getSelectionEnd();
            //Start a stringBuilder so we can work on the text 
            sb = new StringBuilder(backArea.getText());
  
            //Get text from the system clipboard
            String pasteText = getClipboard();
            
            //Remove the string from the area
            sb.replace(st,end,pasteText);
            backArea.setText(sb.toString());
        }

        if(bTitleFieldFocoused)
        {
            //Get the start and end of the user's selection (what is hilighted in the text area)
            int st = titleField.getSelectionStart();
            int end = titleField.getSelectionEnd();
            //Start a stringBuilder so we can work on the text 
            sb = new StringBuilder(titleField.getText());
            
            //Get text from the system clipboard
            String pasteText = getClipboard();
            
            //Remove the string from the area
            sb.replace(st,end,pasteText);
            titleField.setText(sb.toString());   
        }
        
        //repaint all of the text areas so the text appears.
        frontArea.repaint();
        backArea.repaint();
        titleField.repaint();
        this.repaint();
    }
    
    
    
    /**
     * saveOpenCard - This method saves the current card
     *
     */
    private void saveOpenCard()
    {

        String front = frontArea.getText();
        String back = backArea.getText();
        String title = titleField.getText();
        
        //Get the selected card and save any changes if nececary
        //This will return a savestate 1= saved 2 = not if it is saved then
        //The document has changes and needs to be saved
        int ss = cardDeck.get(currentCard).saveIfNececary(title, front, back);
        if(ss == 1)
        {
            //The document has changes and is not saved
            docNotSaved = true;
        }
    }
    
    
   
    /**
     * newCard - creates a new card
     *
     */
    public void newCard()
    {
            JPanel p = drawCardPanel(-1);
            panelDeck.add(p, CARDPANEL);
            cardLayout = (CardLayout)panelDeck.getLayout();
            cardLayout.show(panelDeck, CARDPANEL);
    }

	/**
     * Search Cards - Searches the card deck
     *
     */
    public void searchCards()
    {
            JPanel p = drawSearchPanel();
            panelDeck.add(p, SEARCHPANEL);
            cardLayout = (CardLayout)panelDeck.getLayout();
            cardLayout.show(panelDeck, SEARCHPANEL);
    }
    
    /**
     * openCard - creates a new card
     *
     */
    public void openCard(int i)
    {
            JPanel p = drawCardPanel(i);
            panelDeck.add(p, CARDPANEL);
            cardLayout = (CardLayout)panelDeck.getLayout();
            cardLayout.show(panelDeck, CARDPANEL);
    }
    
    
    /**
     * onQuitAction - Displays a dialoge when the user tries to quit
     */
    public void onQuitAction()
    {
        if(docNotSaved)
        {
            int n = d.showQuitDialog();
                if (n == JOptionPane.NO_OPTION){ this.dispose();}//if the user presses yes then quit
                if (n == JOptionPane.YES_OPTION){ saveCards("");}
                if (n == JOptionPane.CANCEL_OPTION){ }
        }else{
            this.dispose();
        }
    }
    
    /**
     * getClipboard - gets the system clipboard if it is a string
     * @return String, or null
     */
    public static String getClipboard() {
        Transferable t = Toolkit.getDefaultToolkit().getSystemClipboard().getContents(null);
    
        try {
            if (t != null && t.isDataFlavorSupported(DataFlavor.stringFlavor)) {
                String text = (String)t.getTransferData(DataFlavor.stringFlavor);
                return text;
            }
        } catch (UnsupportedFlavorException e) {
        } catch (IOException e) {
        }
        return null;
    }
    
    /**
     * setClipboard - sets the system clipboard
     */
    public static void setClipboard(String str) {
        StringSelection ss = new StringSelection(str);
        Toolkit.getDefaultToolkit().getSystemClipboard().setContents(ss, null);
    }

    
    /**
     * saveCards
     * 
     * This will open a save menu and allow the user to save the currently open deck
     * @param String s, if this is blank this will act as a SaveAs Dialog, if not
     * it will act as a save function, when the user presses ctrl s, the process will 
     * operate in the background.
     * 
     * @return Once done if this succeeded then the docNotSaved boolean will be set to false
     * meaning the program is saved
     */
    public void saveCards(String s)
    {
        if(s.equals(""))//If s is not designated, act as a save as dialog and show the locations you can save
        {
            currentFilePath = d.showSaveDialog(fileFilter, currentFilePath, false, true, false);
            System.out.println("Updating Save Directory To: "+currentFilePath);
            FileO out = new FileO();
            out.writeFile(currentFilePath, cardDeck);
        }
        
        if(!s.equals(""))//If S is designated (NOT "") then just save the file
        {
            FileO out = new FileO();
            out.writeFile(currentFilePath, cardDeck);
        }
        //If somehow S = null set it to equal an empty string
        //This can be caused by the user exiting the save dialog
        //Or a save error.
        if(s.equals(null))
        {
            s = "";
            d.showWarningDialog("Warning","There was a critical error while I\n"+
                                "was trying to save your file.\n"+
                                "Sorry for the inconvinence.");
        }
    }
    
    /**
     * showCardPopup - Generates a popup menu for the card
     *
     * @param MouseEvent e To show where the popup is needed
     */
    public void showCardPopup(MouseEvent e)
    {
        JPopupMenu popper = new JPopupMenu();
        //Cut
            //LookAndFeel
            cardCut = new JMenuItem("Cut");
            //Actions
            cardCut.addActionListener(this);

            //Add
            popper.add(cardCut);
        //Copy
            //LookAndFeel
            cardCopy = new JMenuItem("Copy");
            //Actions
            cardCopy.addActionListener(this);

            //Add
            popper.add(cardCopy);
        //Paste
            //LookAndFeel
            cardPaste = new JMenuItem("Paste");
            //Actions
            cardPaste.addActionListener(this);

            //Add
            popper.add(cardPaste);
            
            popper.show(e.getComponent(), e.getX(), e.getY());

    }
    
    /**
     * deleteCard - Deletes the current card
     *
     * @param  y   the card number
     */
    public void deleteCard()
    {
        //Remove the current card
        cardDeck.remove(currentCard);
        
        //Open the card next in the list
        //But it will now have slid up to fill the spot
        try
        {
        openCard(currentCard);
        }
        //If the card was last in line go the one in front of it,
        //if it was the last one in the deck the current card value
        //will be -1 and a new card will be created
        catch(Exception ex)
        {
            currentCard --;
            openCard(currentCard);
        }
    }
    
    /**
     * deleteCards - Deletes a set of cards top down to avoid unwanted results
     *
     * 
     */
    public void deleteCards()
    {
        
        
        //Get the cards to be deleted
        int[] deleteArray = mainList.getSelectedIndices();
        //Ask the user if they are sure
        int y = d.showYesNoQuestionDialog("Question:",
                                            "<html>Are you sure you want me to delete the selected <b>"
                                            +deleteArray.length+
                                            "</b> card(s) <b>permanatly?</b>");
        
        if(y == JOptionPane.YES_OPTION)
        {
            //Delete them top down so cards dont start fillilng in where one was deleted and mess the whole thing up.
            int j = deleteArray.length;
            j--;
            for(int i = j; i>=0; i--)
            {
                cardDeck.remove(deleteArray[i]);
            }
            drawHome();
        }
    }
    
    /**
     * DrawHome -Draws the home screen
     * 
     */
    private void drawHome()
    {
        JPanel p = drawHomePanel();
            panelDeck.add(p, HOMEPANEL);
            cardLayout = (CardLayout)panelDeck.getLayout();
            cardLayout.show(panelDeck, HOMEPANEL);
    }
    
    /**
     * Import Cards
     *
     * @param  y   a sample parameter for a method
     * @return     the sum of x and y
     */
    public void importCards()
    {
        int yesnooption = d.showYesNoQuestionDialog("Warning","<html>I will import <i><b>all<b></i> of the cards from the chosen file.\n"
                                                                +"<html><b>Proceed?</b>");
        
        if(yesnooption == JOptionPane.YES_OPTION)
        {
            String loc = d.showOpenDialog(fileFilter, "", false, true, false);
            if(loc != null)
            {
                cardDeck = fin.readFile(loc,cardDeck);
            }
            
            drawHome();
        }
    }
    
    /**
     * This inner class is used to define the lists used in the program;
     * 
     */
    static class CellRenderer extends JLabel implements ListCellRenderer {

        public Component getListCellRendererComponent(JList list, Object value, int index, boolean isSelected, boolean cellHasFocus) {
            setText(value.toString());
            if (isSelected) {
                
                setBackground(SystemColor.textHighlight);
				setForeground(SystemColor.textHighlightText );
            } else {
                if(index%2 == 0)//If divisible by 2 with no remainder
                {
                    setBackground(SystemColor.text);
					setForeground(SystemColor.textText );
                }else{
                    setBackground(SystemColor.control);
					setForeground(SystemColor.textText );
                }
            }
            setOpaque(true);
            return this;
        }
    }
}