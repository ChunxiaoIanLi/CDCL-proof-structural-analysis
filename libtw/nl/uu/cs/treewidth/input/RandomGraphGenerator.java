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

public class RandomGraphGenerator implements GraphInput {
	
	private int edgeCount;
	private double cycleChance;
	
	public RandomGraphGenerator(int edgeCount, double cycleChance) {
		this.edgeCount = edgeCount;		
		this.cycleChance = cycleChance;
	}
	public NGraph<InputData> get() throws InputException {
		
		NGraph<InputData> g = new ListGraph<InputData>();
			
		//Make sure the edge count is even
		if( edgeCount % 2 != 0 )
			++edgeCount;
		int nodeCount = 0;
		
		// Create the ground node
		NVertex<InputData> v = new ListVertex<InputData>( new InputData(nodeCount, ""+(nodeCount+1)));
		++nodeCount;
		g.addVertex( v );
		
		
		for( int i=0; i<edgeCount; ++i ) {
			// Pick a random node
			int sourceIndex = (int)(Math.random() * g.getNumberOfVertices());
			NVertex<InputData> source =  g.getVertex( sourceIndex );
			NVertex<InputData> target = null;
			
			if( g.getNumberOfEdges() > 1 && Math.random() < cycleChance ) {
				// Generate a cycle
				boolean found = false;
				for( int n = 0; n < g.getNumberOfVertices(); ++n ) {
					int targetIndex = (int)(Math.random() * g.getNumberOfVertices());
					target = g.getVertex( targetIndex );
					if( targetIndex == sourceIndex )
						continue;
					
					// Check if an edge with the same two nodes is present
					found = true;
					for(NVertex<InputData> neighbor : source) {
						if (neighbor == target)
							found = false;
					}
					
					if( found )
						break;
				}
				if( !found ) {
					target = new ListVertex<InputData>( new InputData(nodeCount, ""+(nodeCount+1)));
					++nodeCount;
					g.addVertex( target );
				}
			} else {
				// Generate a new node as target
				target = new ListVertex<InputData>(new InputData(nodeCount, ""+(nodeCount+1)));
				++nodeCount;
				g.addVertex( target );
			}
			if(source != null && target != null) {
				g.addEdge(source, target);
			}
			
		}		
		return g;
	}

}
