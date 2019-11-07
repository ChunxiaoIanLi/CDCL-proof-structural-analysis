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
import nl.uu.cs.treewidth.output.Output;

public class CliqueGraphGenerator implements GraphInput {
	
	private int x;
	
	public CliqueGraphGenerator(int x) {
		this.x = x;		
	}
	public NGraph<InputData> get() throws InputException {
		
		NGraph<InputData> g = new ListGraph<InputData>();
			
		
		for(int i=0; i<x; ++i) {
		
			NVertex<InputData> v = new ListVertex<InputData>();
			v.data = new InputData();
			v.data.id = i;
			v.data.name = ""+(i+1);
			g.addVertex( v );
			
			for(NVertex<InputData> v2 : g) {
				if( v != v2 ) { 
					g.addEdge(v,v2 );
				}
			}						
		}
		Output.toWindow = true;
		Output.toFile = false;
		
		//Output.present(g,"");
		
		return g;
	}

}
