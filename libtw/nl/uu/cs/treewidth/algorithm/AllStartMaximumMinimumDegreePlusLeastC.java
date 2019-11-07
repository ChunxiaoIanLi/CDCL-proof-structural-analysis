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
public class AllStartMaximumMinimumDegreePlusLeastC<D extends InputData> implements LowerBound<D> {

	protected NGraph<D> graph;
	protected NGraph<D> originalGraph;
	protected int lowerbound;

	/**
	 * Starts out as a lowerbound of -infty; improved to the mindegree
	 * lowerbound once run() is called.
	 */
	public AllStartMaximumMinimumDegreePlusLeastC() {
		lowerbound = Integer.MIN_VALUE;
	}
	
	public String getName() {
		return "All Start MMD+Least-c: All Start Maximum Minimum Degree Plus least-c";
	}

	public void setInput(NGraph<D> g) {
		originalGraph = g;
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
		maxDegree = goRecursive(graph,1);
		if( maxDegree>lowerbound ) lowerbound = maxDegree;		
	}

	public int goRecursive(NGraph<D> graph, int round) {
		++round;
		
		if( graph.getNumberOfVertices()==0 )
			return 0;
		
		int min = Integer.MAX_VALUE;
		//Get all the vertices with min degree
		ArrayList<NVertex<D>> startVertices = new ArrayList<NVertex<D>>();
		for(NVertex<D> v : graph) {
			if( min > v.getNumberOfNeighbors() && v.getNumberOfNeighbors()>0 ) {
				startVertices.clear();
				startVertices.add(v);
				min = v.getNumberOfNeighbors();
			} else 
				if( min == v.getNumberOfNeighbors() ) {
				startVertices.add(v);				
			}	
		}
		int maxDegree = 0;
		
		//Build in check to prevent from going to often in recursion
		int maxIt;
		if(round<3)
			maxIt = startVertices.size();
		else
			maxIt = 1;
		
		int i = 1;
//		For al the vertices: contract with a neighbor and go recursice
		for( NVertex<D> startV : startVertices ) {
			if(maxIt >= i) {
				// Copy the graph to go recursive....not very nice :-S
				NGraph<D> graphcopy = graph.copy();
				
				NVertex<D> newStartV = null;
				for(NVertex<D> v: graphcopy) {
					if( v.data == startV.data) {
						newStartV = v;
					}						
				}
				
				if( newStartV.getNumberOfNeighbors()>maxDegree) {
					maxDegree = newStartV.getNumberOfNeighbors();				
				}
				
				NVertex<D> vertexToContractWith = null;
				
				
				HashSet<NVertex<D>> newStartVNeighbors = new HashSet<NVertex<D>>();
				for(NVertex<D> v : newStartV)
					newStartVNeighbors.add(v);
				
				int sameN = Integer.MAX_VALUE;
				for( NVertex<D> other:  newStartV) {
					int same = 0;
					//Loop over buren van buur
					for(NVertex<D> bb : other)
						if(newStartVNeighbors.contains(bb))
							++same;
					
					if(same<sameN) {
						vertexToContractWith = other;
						sameN = same;
					}					
				}
				
				if( vertexToContractWith!=null )
					graphcopy.contractEdge(newStartV,vertexToContractWith);				
				
				int recresult = 0;
				
				if(graphcopy.getNumberOfEdges() > 0 && graphcopy.getNumberOfVertices()>1)
					recresult = goRecursive(graphcopy, round);
								
				if( recresult>maxDegree)
					maxDegree = recresult;		
				
			}
			i++;
		}		
		return maxDegree;
	}
	
	public int getLowerBound() {
		return lowerbound;
	}
}
