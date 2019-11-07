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

import java.util.HashSet;

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;

/**
 * The MMD+ heuristic with the least-c contraction rul: 
 * when there is a tiebreaker, we contract such that the contracted 
 * vertices have the smallest number of common neighbors.
 * 
 * Reference: 
 * Treewidth: Computational Experiments (Koster, Bodlaender, and van Hoesel)
 * 
 * @author tw team
 *
 */
public class MaximumMinimumDegreePlusLeastC<D extends InputData> implements LowerBound<D> {

	protected NGraph<D> graph;
	protected int lowerbound;
	
	/**
	 * Starts out as a lowerbound of -infty; improved to the mindegree
	 * lowerbound once run() is called.
	 */
	public MaximumMinimumDegreePlusLeastC() {
		lowerbound = Integer.MIN_VALUE;
	}
	
	public String getName() {
		return "MMD+Least-c: Maximum Minimum Degree Plus least-c";
	}

	public void setInput(NGraph<D> g) {
		// This algorithm works straight on the standard Graph data,
		// so just remember it.
		graph = g.copy( );
	}

	public void run() {
		/* MMD(Graph G) ::
		 * H = G
		 * maxmin = 0
		 * while H has at least two vertices do
		 * 	Select a vertex v from H that has minimum degree in H.
		 * 	maxmin = max( maxmin, dH(v) ).
		 * 	Contract v with the neighbour with lowest degree
		 * end while
		 * return maxmin
		 */
		
		 // initial value for finding minimum: higher than any degree
		int maxDegree = 0;		
		int numNodes = graph.getNumberOfVertices();
		for( int i=0; i<numNodes; ++i) {
			
			//Select a vertex from the graph that has minimum degree
			NVertex<D> minDegreeVertex = null;
			int min = Integer.MAX_VALUE;
			for(NVertex<D> v : graph) {
				if( min > v.getNumberOfNeighbors() ) {
					minDegreeVertex = v;
					min = v.getNumberOfNeighbors();
				}				
			}
			if( minDegreeVertex != null ){
				//if the the maxdegree of the selected vertex > current high: 
				//set maxdegree as new lowerbound
				if( minDegreeVertex.getNumberOfNeighbors()>maxDegree) {
					maxDegree = minDegreeVertex.getNumberOfNeighbors();					
				}
				
				NVertex<D> vertexToContractWith = null;
				
				HashSet<NVertex<D>> newStartVNeighbors = new HashSet<NVertex<D>>();
				for(NVertex<D> v : minDegreeVertex)
					newStartVNeighbors.add(v);
				
				int sameN = Integer.MAX_VALUE;
				for( NVertex<D> other:  minDegreeVertex) {
					//Loop over buren van buur
					int same = 0;
					for(NVertex<D> bb : other)
						if(newStartVNeighbors.contains(bb))
							++same;
					
					if(same<sameN) {
						vertexToContractWith = other;
						sameN = same;
					}					
				}
				if( vertexToContractWith!=null ) {
					graph.contractEdge(minDegreeVertex,vertexToContractWith);					
				}				
			}			
		}		
		if( maxDegree>lowerbound ) lowerbound = maxDegree;		
		
	}

	public int getLowerBound() {
		return lowerbound;
	}
}
