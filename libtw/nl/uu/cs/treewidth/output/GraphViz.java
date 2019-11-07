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

import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;

import javax.imageio.ImageIO;

public class GraphViz {
	
	public static BufferedImage render( String dotSource ) {
		
		System.out.print(".");
		
		BufferedImage image = null;
		
		// run the graphviz commandline
		Runtime sys = Runtime.getRuntime();
		Process neato;
		try {
			neato = sys.exec( "dot -Tpng" );
		
			InputStream fromNeato = neato.getInputStream();
			OutputStream toNeato = neato.getOutputStream();
				
		    PrintWriter writer = new PrintWriter(toNeato);
			writer.write( dotSource );
			writer.close();
	
			image = ImageIO.read( fromNeato );
	
		} catch (IOException e) {}
		
		return image;
		
	}

}
