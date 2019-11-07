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
 * Used graphstructure: NeighborHashSetGraph
 * 
 * 
 * The 'MinorMinWidth' lower bound.
 * Reference: A Complete Anytime Algorithm for Treewidth
 *            Vibhav Gogate and Rina Dechter
 * 
 * The algorithm repeativly contracts the lowest degree vertex with a lowest degree neighbor.
 * The lowerbound is the maximum degree of the selected lowest degree vertices at the time of contraction. 
 * 
 * @author tw team
 *
 */
public class MinorMinWidth< D extends InputData > implements LowerBound<D> {

	protected NGraph<D> graph;
	protected int lowerbound;
	
	
	/**
	 * Starts out as a lowerbound of -infty; improved to the mindegree
	 * lowerbound once run() is called.
	 */
	public MinorMinWidth() {
		lowerbound = Integer.MIN_VALUE;
	}
	
	
	public String getName() {
		return "MinorMinWidth";
	}
	

	public void setInput( NGraph<D> g ) {
		graph = g.copy();
	}

	
	/**
	 * Method runs the algorithm and sets the lowerbound.
	 *
	 */
	public void run() {
		/*
		 * 1. lb=0;
		 * 2. Repeat
		 *   (a) Contract the edge between a minimum degree
		 *       vertex v and u 2 N(v) such that the degree of
		 *       u is minimum in N(v) to form a new graph G0.
		 *   (b) lb = MAX(lb; degree_G(V))
		 *   (c) Set G to G'
		 * 3. Until no vertices remain in g.
		 * 4. return lb
		 */
		
		while( graph.getNumberOfVertices()>0 ) {
			//Find the vertex with lowest degree
			int min = Integer.MAX_VALUE;
			NVertex<D> z = null;
			for( NVertex<D> v : graph ) {
				if( v.getNumberOfNeighbors() < min  &&  v.getNumberOfNeighbors() > 0) { 
					z = v;
					min = v.getNumberOfNeighbors();
				}
			}
			
			//If there are no edges left in the Graph: we are done
			if(z==null)
				return;
			
			if(min > lowerbound)
				lowerbound = min;
			
			//Find the neighbour with lowest degree
			min = Integer.MAX_VALUE;
			NVertex<D> contractVertex = null;
			for( NVertex<D> other : z ) {
				if( other.getNumberOfNeighbors() < min ) { 
					min = other.getNumberOfNeighbors();
					contractVertex = other;
				}
			}	
			//Contract the Edge from the graph
			graph.contractEdge( new NEdge<D>( z, contractVertex ) );			
		}		
	}

	
	/**
	 * 
	 * @return The current lowerbound
	 */
	public int getLowerBound() {
		return lowerbound;
	}
}
