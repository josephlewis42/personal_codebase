using System;
using Gtk;
using System.Text.RegularExpressions;
using System.Collections;
using System.Net.Mail;
using System.Collections.Generic;
using System.Text;
using GtkSharp;
using GLib;
using System.Net;
using System.Security.Cryptography.X509Certificates;
using System.Net.Security;
using System.Net.Mime;
using System.Threading;

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
	
	protected virtual void send_mail_event(object sender, System.EventArgs e)
	{
		send_mail ();
		//System.Threading.Thread firstRunner = new System.Threading.Thread (new ThreadStart (this.send_mail));
		//firstRunner.Start();
	}
	
	protected virtual void send_mail ()
	{
		string username = userEntry.Text;
		string password = passwordEntry.Text;
		string subject = subject_entry.Text;
		string body = body_text.Buffer.Text;
				
		Gtk.Application.Invoke (delegate {
			message_progress.Fraction = 0;
        });
			MessageDialog mdm = new MessageDialog(this, 
            DialogFlags.DestroyWithParent, MessageType.Info, 
            ButtonsType.Close, "My interface may 'freeze' for a moment while I'm sending emails, don't worry, this is normal.");
        	mdm.Run();
        	mdm.Destroy();
		
		try {
			SmtpClient SmtpServer = new SmtpClient("smtp.gmail.com");
			SmtpServer.Port = 587;
			SmtpServer.Credentials = new System.Net.NetworkCredential(username.Split('@')[0], password);
			SmtpServer.EnableSsl = true;
			ServicePointManager.ServerCertificateValidationCallback = delegate(object s, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors) { return true; };
			
			ArrayList people = grabEmails();
			double percent_per_person = people.Count/100.0;
			
			Gtk.Application.Invoke (delegate {
				message_progress.Text = "Running";
			});

			foreach(string person in people)
			{
				MailMessage mail = new MailMessage();
				mail.From = new MailAddress(username);
				mail.To.Add(person);
				mail.Subject = subject;
				mail.Body = body;
				mail.IsBodyHtml = htmlCheck.Active;
				if(attach_box.Text != "")
					mail.Attachments.Add(new Attachment(attach_box.Text, MediaTypeNames.Application.Octet));
				
				SmtpServer.Send(mail);
				
				Gtk.Application.Invoke (delegate {
					message_progress.Fraction += percent_per_person;
        		});		
			}
		} catch(System.Net.Mail.SmtpException){
			Gtk.Application.Invoke (delegate {

				MessageDialog md = new MessageDialog(this, 
	            	DialogFlags.DestroyWithParent, MessageType.Warning, 
	            	ButtonsType.Close, "I couldn't connect to the server, check that you are connected to the Internet and your username and password are right.");
	        	md.Run();
	        	md.Destroy();
			});
			return;
		} catch(Exception ex) {
			Gtk.Application.Invoke (delegate {
				MessageDialog md = new MessageDialog(this, 
	            	DialogFlags.DestroyWithParent, MessageType.Warning, 
	            	ButtonsType.Close, ex.ToString());
	        	md.Run();
	        	md.Destroy();
			});
			return;
		}
		Gtk.Application.Invoke (delegate {
			message_progress.Fraction = 0;
			message_progress.Text = "Done";
			
			MessageDialog md = new MessageDialog(this, 
            	DialogFlags.DestroyWithParent, MessageType.Info, 
            	ButtonsType.Close, "Finished Sending Emails");
	        md.Run();
	        md.Destroy();
        });
	}
	
	
	protected virtual void leave_to (object o, Gtk.FocusOutEventArgs args)
	{
		grabEmails();
	}
	
	protected virtual ArrayList grabEmails()
	{
		// Remove all of the crap.
		string input = email_entry.Buffer.Text;
		string pattern = @"[^a-zA-Z0-9@.\+\-]+";
		string emailpattern = @"[a-zA-Z0-9.\+\-]+@[a-zA-Z0-9\-_]+\.[a-zA-Z0-9]+";

		ArrayList outputs = new ArrayList();
		
		foreach (string result in Regex.Split(input, pattern)) 
   			if(Regex.IsMatch(result,emailpattern))
				outputs.Add(result);
			else
				if(result.Trim() != "")
				{
					email_expand.Expanded = true;
					fix_email_entry.Buffer.Text += "" + result + "\n";
				}
		
		email_entry.Buffer.Text = "";
		
		//uniquify the emails
		ArrayList noDups = new ArrayList();
		foreach(string strItem in outputs)
			if (!noDups.Contains(strItem.Trim()))
				noDups.Add(strItem.Trim());
		noDups.Sort();

		// Split in to email addresses.
		foreach(string tmp in noDups)
			email_entry.Buffer.Text += tmp + ", ";
		
		return outputs;
	}
	
	protected virtual void leave_body (object o, Gtk.FocusOutEventArgs args)
	{
		checkHTML();
	}
	
	/*
	 * Checks if the input is HTML, if so sets the HTML flag.
	 */
	protected virtual void checkHTML()
	{
		String bt = body_text.Buffer.Text.ToLower();
		bt = bt.Trim();

		if( bt.StartsWith("<html>"))
			htmlCheck.Active = true;
		else
			htmlCheck.Active = false;
	}
	
	protected virtual void add_attachment (object sender, System.EventArgs e)
	{
		FileChooserDialog Fcd = new FileChooserDialog ("Open file", null, FileChooserAction.Open);

		Fcd.AddButton(Stock.Cancel, ResponseType.Cancel);
		Fcd.AddButton(Stock.Open, ResponseType.Ok);
		
		ResponseType RetVal = (ResponseType)Fcd.Run();

		if (RetVal == ResponseType.Ok)
			attach_box.Text = Fcd.Filename;
		
		Fcd.Destroy();
	}
	
	protected virtual void del_attachment (object sender, System.EventArgs e)
	{
		attach_box.Text = "";
	}
}