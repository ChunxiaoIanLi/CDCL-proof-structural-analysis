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

import java.awt.Cursor;
import java.awt.Graphics;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;

@SuppressWarnings("serial")
public class NeatoViewer extends JPanel implements MouseMotionListener {

	public static void present( String dot, String title, int x, int y, boolean toFile, boolean toWindow ) {
				
		try {
			
			NeatoViewer viewer = null; 
			
			if( toWindow ) {
				// ===== Make a window
				JFrame frame = new JFrame();
			    frame.setTitle( title );
			    frame.setSize( 500, 750 );
			    frame.addWindowListener(new WindowAdapter() {
			    	public void windowClosing(WindowEvent e) {
			    		System.exit(0);
			        }
			    });
			    frame.addKeyListener(new KeyAdapter() {
			    	public void keyReleased(KeyEvent e) {
			    		if( e.getKeyCode() == KeyEvent.VK_ESCAPE ) System.exit(0);
			    	}
			    });
	
			    viewer = new NeatoViewer(frame);
			    frame.getContentPane().add( viewer );
			    frame.setLocation( x, y );
			    frame.setVisible(true);
			}
			
		    // ===== Run GraphViz
		
		    BufferedImage image = GraphViz.render( dot );

		    if( toFile ) ImageIO.write( image, "png", new File(title+".png") );
		    if( toWindow ) {
		    	viewer.setImage( image, title );
		    	viewer.repaint();
		    }
		    
		} catch( IOException e ) {
			e.printStackTrace();
		}
	}
	
	JFrame parent;
	String title;
	BufferedImage image;
	int mouseX, mouseY;
	int draggedX, draggedY;
		
	NeatoViewer( JFrame parent ) {
        this.parent = parent;
               
        addMouseMotionListener( this );
        draggedX = 0;
        draggedY = 0;
	}
	
	public void setImage( BufferedImage image, String title ) {
		this.image = image;
		this.title = title;
	}
	
	public void paint( Graphics gr ) {	
		int w = getWidth();
		int h = getHeight();
		gr.clearRect(0,0,w,h);
		int x = w/2;
		int y = h/2;
		if( image!=null ) {
			x -= image.getWidth() / 2;
			y -= image.getHeight() / 2;
			x += draggedX;
			y += draggedY;
			gr.drawImage( image, x, y, null, null );
		} else {
			gr.drawString( "Waiting for GraphViz to make the image ...", x-130, y );
		}
	}
	
	public void mouseMoved(MouseEvent e ){
		setCursor(new Cursor(Cursor.HAND_CURSOR));
		mouseX = e.getX();
		mouseY = e.getY();
	}
	public void mouseDragged(MouseEvent e) {
		setCursor(new Cursor(Cursor.MOVE_CURSOR));
		int newX = e.getX();
		int newY = e.getY();
		draggedX += newX-mouseX;
		draggedY += newY-mouseY;
		mouseX = newX;
		mouseY = newY;
		repaint();
	}

}
