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

import java.util.ArrayList;

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.ListGraph;
import nl.uu.cs.treewidth.ngraph.ListVertex;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;

/**
 * The algorithm repeativly contracts the lowest degree vertex with a lowest degree neighbor.
 * The lowerbound is the maximum degree of the selected lowest degree vertices at the time of contraction. 
 * 
 * This algorithm is optimized to be used with the QuickBB algorithm.
 * It does not really contract the edges from the graph, but uses a copy of the neighbors of every vertex.
 * 
 * 
 * The 'MinorMinWidth' lower bound.
 * Reference: A Complete Anytime Algorithm for Treewidth
 *            Vibhav Gogate and Rina Dechter
 * @author tw team
 *
 */
public class AllStartMinorMinWidth_QuickBB<D extends InputData>  {

	protected NGraph<QuickBB<D>.QuickBBData> graph;
	protected int lowerbound;
	
	/**
	 * Starts out as a lowerbound of -infty; improved to the mindegree
	 * lowerbound once run() is called.
	 */
	public AllStartMinorMinWidth_QuickBB() {
		lowerbound = Integer.MIN_VALUE;
	}
	
	public String getName() {
		return "All Start Minor Min Width (QuickBB Version)";
	}

	public void setInput(NGraph<QuickBB<D>.QuickBBData> g) {
		graph = g;		
	}

	@SuppressWarnings("unchecked")
	public void run() {
		/*
		 * 1. lb=0;
		 * 2. Repeat
		 *   (a) Contract the edge between a minimum degree
		 *       vertex v and u in N(v) such that the degree of
		 *       u is minimum in N(v) to form a new graph G0.
		 *   (b) lb = MAX(lb; degree_G(V))
		 *   (c) Set G to G'
		 * 3. Until no vertices remain in g.
		 * 4. return lb
		 */
		
//		Find the vertex with lowest degree
		ArrayList<NVertex<QuickBB<D>.QuickBBData>> startVertices = new ArrayList<NVertex<QuickBB<D>.QuickBBData>>();
		
		int min = Integer.MAX_VALUE;
		for( NVertex<QuickBB<D>.QuickBBData> v : graph ) {
			if( v.getNumberOfNeighbors() < min  &&  v.getNumberOfNeighbors() > 0) { 
				startVertices.clear();
				startVertices.add(v);
				min = v.getNumberOfNeighbors();
			} else if(v.getNumberOfNeighbors() == min) {
				startVertices.add(v);
			}
		}
		
		for(NVertex<QuickBB<D>.QuickBBData> startV : startVertices) {
			
			// TODO: the following is not so nice.
			// maybe make it work on other graphs someday.
			// not worth it right now.
			if( !(graph instanceof ListGraph) ) {
				throw new UnsupportedOperationException();
			} else {
				for(NVertex<QuickBB<D>.QuickBBData> v : graph) {
					ListVertex<QuickBB<D>.QuickBBData> v3 = (ListVertex<QuickBB<D>.QuickBBData>) v;
					v.data.vertices = (ArrayList<NVertex<QuickBB<D>.QuickBBData>>) v3.neighbors.clone();
				}
			}
			int round = 0;
			
			boolean done = false;
			while( ! done ) {
				//Find the vertex with lowest degree
				NVertex<QuickBB<D>.QuickBBData> z = null;
				if(round==0) {
					z = startV;
				} else {
					min = Integer.MAX_VALUE;
					for( NVertex<QuickBB<D>.QuickBBData> v : graph ) {
						if( v.data.vertices.size() < min  && v.data.vertices.size() > 0) { 
							z = v;
							min = v.data.vertices.size();
						}
					}
				}
				
				if(z==null)  {
					done =true;
					return;
				}
				
				if(min > lowerbound)
					lowerbound = min;
				
				//Find the neighbour with lowest degree
				min = Integer.MAX_VALUE;
				NVertex<QuickBB<D>.QuickBBData> contractVertex = null;
				for( NVertex<QuickBB<D>.QuickBBData> e : z.data.vertices ) {
					if( e.data.vertices.size() < min && e.data.vertices.size() > 0 ) { 
						min = e.data.vertices.size();
						contractVertex = e;
					}
				}			
						
				//Contract the Edge from the graph
				contractEdge(z,contractVertex);			
				round++;
			}
		}
	}
	
	public void contractEdge(NVertex<QuickBB<D>.QuickBBData> v1, NVertex<QuickBB<D>.QuickBBData> v2) {
		NVertex<QuickBB<D>.QuickBBData> v;
		NVertex<QuickBB<D>.QuickBBData> w;
		if(v1.data.vertices.size() > v2.data.vertices.size()) {
			v = v1;
			w = v2;
		} else {
			v = v2;
			w = v1;
		}
		w.data.vertices.remove(v);
		v.data.vertices.remove(w);
		for(NVertex<QuickBB<D>.QuickBBData> x : w.data.vertices) {
			if(! v.data.vertices.contains(x)) {
				v.data.vertices.add(x);
				x.data.vertices.add(v);
			}				
		}
		removeVertex(w);		
	}
	
	public void removeVertex(NVertex<QuickBB<D>.QuickBBData> v1) {
		for(NVertex<QuickBB<D>.QuickBBData> v : v1.data.vertices) {
			v.data.vertices.remove(v1);
		}
		v1.data.vertices.clear();
	}

	public int getLowerBound() {
		return lowerbound;
	}

}
