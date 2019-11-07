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

import java.util.LinkedList;

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;
import nl.uu.cs.treewidth.ngraph.NVertexOrder;

/**
 * The GreedyFillIn algorithm computes a permutation and at the same time derives an upperbound.<br/>
 * It does this by eliminating the vertex for which we have to add the lowest number of edges
 * when we would eliminate the vertex. This is done until the graph is empty.<br/>
 * 
 * Reference paper: Treewidth Computations I. Upper Bounds, Hans L. Bodlaender and Arie M.C.A. Koster (to appear).
 * 
 * @author tw team
 *
 */
public class GreedyFillIn<D extends InputData> implements Permutation<D>, UpperBound<D> {

	private NVertexOrder<D> permutation;
	private NGraph<GreedyData> graph;
	private int upperBound;
	private boolean checkDegreeZero;
	
	public class GreedyData {
		public NVertex<D> original;
		public int edgesToAdd;
		public GreedyData( NVertex<D> from ) {
			original = from;
			edgesToAdd = 0;
		}
		public String toString(){
			return original.data.name;
		}
	}
	
	class MyConvertor implements NGraph.Convertor<D,GreedyData> {
		public GreedyData convert( NVertex<D> old ) {
			GreedyData d = new GreedyData( old );
			return d;
		}
	}
	
	public GreedyFillIn(){
		permutation = new NVertexOrder<D>();
		upperBound = Integer.MAX_VALUE;
		checkDegreeZero = true;
	}
	
	public GreedyFillIn(boolean checkDegreeZero){
		permutation = new NVertexOrder<D>();
		upperBound = Integer.MAX_VALUE;
		this.checkDegreeZero = checkDegreeZero;
	}
	
	public NVertexOrder<D> getPermutation() {
		return permutation;
	}

	public String getName() {
		return "GreedyFillIn";
	}

	public void setInput(NGraph<D> g) {
		graph = g.copy(new MyConvertor());
	}

	public void run() {
		//TODO: make more efficient implementation
		// This can be done by calculating the overlap
		// of neighbors between each pair of vertices.
		
		upperBound = Integer.MIN_VALUE;
		if (checkDegreeZero){
			// Check if there are vertices with degree 0. We can remove them immediately.
			LinkedList<NVertex<GreedyData>> list = new LinkedList<NVertex<GreedyData>>();
			for (NVertex<GreedyData> v: graph){
				if (v.getNumberOfNeighbors() == 0)
					list.add(v);
			}
			for (NVertex<GreedyData> v: list){
				permutation.order.add(v.data.original);
				graph.eliminate(v);
				//System.out.println("Eliminated vertex "+v.data+" in preliminary degree check.");
			}
		}
		while (graph.getNumberOfVertices() > 0){
			NVertex<GreedyData> selectedVertex = null;
			int minNonAdjNeighbors = Integer.MAX_VALUE; 
			// Find the vertex for which we have to add the lowest number of edges
			// when we would eliminate this vertex in the graph.
			for(NVertex<GreedyData> v: graph){
				int nonAdjNeighbors = virtualElimination(v);
				if (nonAdjNeighbors == 0){
					// If there is a vertex with value 0, we can not find a better one.
					selectedVertex = v;
					break;
				} else if (nonAdjNeighbors < minNonAdjNeighbors){
					selectedVertex = v;
					minNonAdjNeighbors = nonAdjNeighbors;
				}
			}
						
			permutation.order.add(selectedVertex.data.original);
			upperBound = Math.max(upperBound,selectedVertex.getNumberOfNeighbors());		
			// Eliminate the vertex in the graph.
			graph.eliminate(selectedVertex);
			//System.out.println("Deleted vertex "+selectedVertex.data+" of degree " + selectedVertex.getNumberOfNeighbors());
		}
	}
	
	/**
	 * This function computes the number of edges added when you would
	 * eliminate this vertex. It does not eliminate the vertex; that's why
	 * it is 'virtual' :).
	 * 
	 * @param v The vertex to eliminate.
	 * @return The number of edges added when you would eliminate this vertex.
	 */
	private int virtualElimination(NVertex<GreedyData> v){
		int edgesAdded = 0;
		LinkedList<NVertex<GreedyData>> neighbors = new LinkedList<NVertex<GreedyData>>();
		for (NVertex<GreedyData> other: v){
			// Only check for neighbors that come 'before' this neighbor to avoid edges getting counted twice.
			for(NVertex<GreedyData> n: neighbors){
				// If there is no edge, we should add it when we eliminate this vertex.
				if (!other.isNeighbor(n))
					++edgesAdded;
			}
			neighbors.add(other);
		}
		return edgesAdded;
	}

	
	public int getUpperBound() {
		return upperBound;
	}
	
}
