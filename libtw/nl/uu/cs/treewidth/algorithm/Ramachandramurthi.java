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
 
package nl.uu.cs.treewidth.algorithm;

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NEdge;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;

/**
 * 
 * The 'Ramachandramurthi' lower bound.
 * When G = (V;E) is a clique, the lowerbound equals the number of vertices minus 1; 
 * and when G is not a clique, the lowerbound equals the minimum over all pairs 
 * of non-adjacent vertices v, w, of the maximum of the degree of v and w. * 
 * 
 * Reference: The Structure and Number of Obstructions to Treewidth
 * 			  Siddharthan Ramachandramurthi
 * 
 * @author tw team
 *
 */
public class Ramachandramurthi< D extends InputData >implements LowerBound<D> {

	protected NGraph<D> graph;
	protected int lowerbound;
	
	
	/**
	 * Starts out as a lowerbound of -infty; improved to the mindegree
	 * lowerbound once run() is called.
	 */
	public Ramachandramurthi() {
		lowerbound = Integer.MIN_VALUE;
	}
	
	
	public String getName() {
		return "Ramachandramurthi";
	}

	
	public void setInput(NGraph<D> g) {
		graph = g.copy(  );
	}

	
	/**
	 * Method runs the algorithm and sets the lowerbound.
	 *
	 */
	public void run() {
		/* Ramachandramurthi, when
		 * G = (V;E) is a clique, the number of vertices minus 1; and when G is not
		 * a clique, the minimum over all pairs of non-adjacent vertices v, w, of the
		 * maximum of the degree of v and w.
		 */
		
		//Check if the graph is a clique
		boolean clique = true;
		for(NVertex<D> v : graph)
			if(v.getNumberOfNeighbors() != graph.getNumberOfVertices()-1)
				clique = false;
		if(clique) {
			lowerbound = graph.getNumberOfVertices()-1;
			return;
		}
		
		//Create a n*n matrix. Each value (a,b) is true iff there is a edge between a and b
		boolean [][] m = new boolean [graph.getNumberOfVertices()][graph.getNumberOfVertices()];
		
		//Check the edges
		for(NEdge<D> e: graph.edges()) {
			m[e.a.data.id][e.b.data.id] = true;
			m[e.b.data.id][e.a.data.id] = true;
		}
		
		//Find the min max degree
		int minDegree = graph.getNumberOfVertices();
		for(int i=0; i<graph.getNumberOfVertices(); ++i) {
			for(int j=0; j<graph.getNumberOfVertices(); ++j) {
				if(i != j) {
					NVertex<D> v1 = graph.getVertex(i);
					NVertex<D> v2 = graph.getVertex(j);
					
					if(!m[i][j]) {
						//Non-adjacent
						int max;
						if(v1.getNumberOfNeighbors() > v2.getNumberOfNeighbors())
							max = v1.getNumberOfNeighbors();
						else
							max = v2.getNumberOfNeighbors();
						if( max < minDegree ) minDegree = max;							
					}
				}				
			}
		}			
				
		// don't lower the lower bound if we already know a
		// better one.
		if( minDegree>lowerbound ) lowerbound = minDegree;
		
	}

	public int getLowerBound() {
		return lowerbound;
	}
}
