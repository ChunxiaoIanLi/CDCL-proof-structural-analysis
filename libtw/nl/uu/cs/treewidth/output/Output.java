/*
 * Copyright (C) 2006 
 * Thomas van Dijk
 * Jan-Pieter van den Heuvel
 * Wouter Slob
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */
 
package nl.uu.cs.treewidth.output;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.HttpURLConnection;
import java.net.InetAddress;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.net.UnknownHostException;
import java.util.Date;

import nl.uu.cs.treewidth.graph.Graph;
import nl.uu.cs.treewidth.graph.NeighborHashSetGraph;
import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NTDBag;

public abstract class Output {
	
	public static boolean toFile = false;
	public static boolean toWindow = true;

	public static <Data> void present( Graph<Data> g, String title ) {
		String dotCode = DotWriter.format( g );
		presentMain( dotCode, title );
	}
	public static <Data> void present( NeighborHashSetGraph<Data> g, String title ) {
		String dotCode = DotWriter.format( g );
		presentMain( dotCode, title );
	}
	public static <Data> void present( NGraph<Data> g, String title ) {
		String dotCode = DotWriter.format( g );
		presentMain( dotCode, title );
	}
	public static void presentTD( NGraph<NTDBag<InputData>> g, String title) {
		String dotCode = DotWriter.formatTD( g );
		presentMain( dotCode, title );
	}	
	
	static int id = 1;
	static int windowSpawnX = 0;
	static int windowSpawnY = 0;
	protected static void presentMain( String dotCode, String title ) {
		NeatoViewer.present( dotCode, id+++"_"+title, windowSpawnX, windowSpawnY, toFile, toWindow );
		windowSpawnX += 32;
		windowSpawnY += 16;	
	}
	
	public static void waitForEnter() {
		BufferedReader user = new BufferedReader(new InputStreamReader(System.in));
		try {
			user.readLine();
		} catch (IOException e) {}
	}
	
	protected static String bugreportURL = "http://projects.piozum.nl/exppost/todo.php";
	protected static int confirmTimeout = 3000;
	protected static boolean submitBugs = true;
	public static void bugreport( String msg ) {
		
		// print to stderr
		PrintStream out = System.err;
		BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		out.println();
		out.println( "********************************************************************************" );
		out.println( "[BUG] " + msg );
		out.println( "********************************************************************************" );
		
		// try to add a todo on the project website
		out.println();
		if( confirmTimeout>0 ) {
			// TODO do a timeout, now just blocks. don't know how to timeout on reading stdin
			out.println( "Do you want to upload this bugreport to the online TODO list?" );
			boolean chosen = false;
			while( !chosen ) {
				chosen = true; // tentatively set chosen to true; might go back to false later in the loop
				out.println( "[Y]es to this bug" );
				out.println( "[N]o to this bug" );
				out.println( "yes to [A]ll bugs this run" );
				out.println( "n[O] to all bugs this run" );
				out.print( "? " );
				char choice = ' ';
				try {
					choice = in.readLine().charAt(0);
				} catch (IOException e) {}
				switch( choice ) {
				case 'y': case 'Y':
					submitBugs = true;
					break;
				case 'n': case 'N':
					submitBugs = false;
					break;
				case 'a': case 'A':
					submitBugs = true;
					confirmTimeout = 0; // don't ask again
					break;
				case 'o': case 'O':
					submitBugs = false;
					confirmTimeout = 0; // don't ask again
					break;
				default:
					chosen = false;
				}
			}
		}
		
		if( submitBugs ) {
			out.println();
			out.print( "Phone home with bugreport ... " );
			try {
	
				URL url = new URL( bugreportURL );
				URLConnection connection = url.openConnection();
				if (connection instanceof HttpURLConnection) {
					HttpURLConnection httpConnection = (HttpURLConnection)connection;
					httpConnection.setRequestMethod("POST");
					httpConnection.setDoOutput(true);
					httpConnection.setUseCaches (false);
					httpConnection.connect();
					PrintStream post = new PrintStream( httpConnection.getOutputStream() );
				    
					String encoding = "UTF-8";
					post.print( "action=add" );
					post.print( "&label=AutoReport" );
					post.print( "&priority=4" );
					InetAddress here = InetAddress.getLocalHost();
					String info = "[Generated by " + here + " on " + new Date() +  "]   ";
					post.println( "&description=" + URLEncoder.encode(info+msg,encoding) );
	
					int response = httpConnection.getResponseCode();
					out.print( "HTTP response " + response );
					
					post.flush();
					post.close();
					
					httpConnection.disconnect();
				}
			} catch (UnknownHostException e) {
				out.print( "but could not connect to home." );
			} catch (IOException e) {
				out.print( "but communication failed." );
			}
		}
		
	}
	
}
