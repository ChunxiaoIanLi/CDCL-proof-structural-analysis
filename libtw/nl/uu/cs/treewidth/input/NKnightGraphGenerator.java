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
 
package nl.uu.cs.treewidth.input;

import nl.uu.cs.treewidth.ngraph.ListGraph;
import nl.uu.cs.treewidth.ngraph.ListVertex;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;

public class NKnightGraphGenerator implements GraphInput {
	
	private int x;
	
	public NKnightGraphGenerator(int x) {
		this.x = x;		
	}
	public NGraph<InputData> get() throws InputException {
		
		NGraph<InputData> g = new ListGraph<InputData>();
			
		//Create the vertices
		for(int i=0; i<x*x; ++i) {		
			NVertex<InputData> v = new ListVertex<InputData>();
			v.data = new InputData();
			v.data.id = i;
			v.data.name = ""+(i+1);
			g.addVertex( v );							
		}
		
		for(int a=0; a<x; a++ ) { //rows
			for(int b=0; b< x; b++) { //columns
				//(-2+1)
				if( b-2 >= 0 && a+1 < x )
					g.ensureEdge(g.getVertex(a*x+b),g.getVertex(((a+1)*x+(b-2))));
				
				//(-1+2)
				if( b-1 >= 0 && a+2 < x )
					g.ensureEdge(g.getVertex(a*x+b),g.getVertex(((a+2)*x+(b-1))));
				
				//(+1+2)
				if( b+1 < x && a+2 < x )
					g.ensureEdge(g.getVertex(a*x+b),g.getVertex(((a+2)*x+(b+1))));
				
				//(+2+1)
				if( b+2 < x && a+1 < x )
					g.ensureEdge(g.getVertex(a*x+b),g.getVertex(((a+1)*x+(b+2))));
			}
		}
		
		g.printGraph(true,false);
		return g;
	}

}
