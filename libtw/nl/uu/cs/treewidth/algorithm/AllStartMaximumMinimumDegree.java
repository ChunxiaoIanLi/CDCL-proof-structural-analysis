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
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;

/**
 * The degeneracity of a graph is a lower bound for treewidth. 
 * This is the maximum over all subgraphs of G of the minimum degree. It can be computed as follows: repeatedly remove the vertex of minimum degree. 
 * The maximum degree of a vertex at time of removal is the degeneracy.
 * 
 * Reference: 
 * Treewidth: Computational Experiments (Koster, Bodlaender, and van Hoesel)
 * 
 * @author tw team
 */
public class AllStartMaximumMinimumDegree<D extends InputData> implements LowerBound<D> {

	protected NGraph<D> graph;
	protected int lowerbound;
	
	/**
	 * Starts out as a lowerbound of -infty; improved to the mindegree
	 * lowerbound once run() is called.
	 */
	public AllStartMaximumMinimumDegree() {
		lowerbound = Integer.MIN_VALUE;
	}
	
	public String getName() {
		return "All Start Maximum Minimum Degree";
	}

	
	public void setInput(NGraph<D> g) {
		graph = g.copy( );
	}

	public void run() {
		/* MMD(Graph G) ::
		 * H = G
		 * maxmin = 0
		 * while H has at least two vertices do
		 * 	Select a vertex v from H that has minimum degree in H.
		 * 	maxmin = max( maxmin, dH(v) ).
		 * 	Remove v and its incident edges from H.
		 * end while
		 * return maxmin
		 */
		
		 // initial value for finding minimum: higher than any degree
		
		int maxDegree = goRecursive(graph);
		if( maxDegree>lowerbound ) lowerbound = maxDegree;
		
	}
	
	private int goRecursive(NGraph<D> g) {
		//List with start vertices with min degree
		ArrayList<NVertex<D>> startVertices = new ArrayList<NVertex<D>>();
		
		int min = Integer.MAX_VALUE;
		for( NVertex<D> v : g ) {
			if( v.getNumberOfNeighbors() < min  &&  v.getNumberOfNeighbors() > 0) { 
				startVertices.clear();
				startVertices.add(v);
				min = v.getNumberOfNeighbors();
			}
		}
		int maxDegree = 0;
		for(NVertex<D> startV : startVertices) {
			
			NGraph<D> graphcopy = g.copy();
			NVertex<D> minDegreeVertex = null;
			
			//Zoek de startV in de nieuwe graaf
			for(NVertex<D> newV : graphcopy) {
				if(newV.data == startV.data)
					minDegreeVertex = newV;
			}					
			 
				
			if( minDegreeVertex != null ){
				if( minDegreeVertex.getNumberOfNeighbors()>maxDegree) {
					maxDegree = minDegreeVertex.getNumberOfNeighbors();
				}
				graphcopy.removeVertex(minDegreeVertex);				
			}
				
			int recResult = goRecursive(graphcopy);
			maxDegree = Math.max(maxDegree,recResult);			
		}
		return maxDegree;
	}

	public int getLowerBound() {
		return lowerbound;
	}
}
