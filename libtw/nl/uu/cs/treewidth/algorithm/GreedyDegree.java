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
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;
import nl.uu.cs.treewidth.ngraph.NVertexOrder;

/**
 * The GreedyDegree algorithm computes a permutation and at the same time derives an upperbound.<br/>
 * It does this by eliminating the vertex with the smallest degree until the graph is empty.<br/>
 * 
 * Reference paper: Treewidth Computations I. Upper Bounds, Hans L. Bodlaender and Arie M.C.A. Koster (to appear).
 * 
 * @author tw team
 *
 */
public class GreedyDegree< D extends InputData > implements Permutation<D>, UpperBound<D> {

	protected NVertexOrder<D> permutation;
	protected NGraph<GreedyData> graph;
	protected int upperBound;
	
	public class GreedyData {
		public NVertex<D> original;
		public GreedyData( NVertex<D> from ) {
			original = from;
		}
	}
	class MyConvertor implements NGraph.Convertor<D,GreedyData> {
		public GreedyData convert( NVertex<D> old ) {
			GreedyData d = new GreedyData( old );
			return d;
		}
	}
	
	public GreedyDegree(){
		permutation = new NVertexOrder<D>();
		upperBound = Integer.MAX_VALUE;
	}
	
	public NVertexOrder<D> getPermutation() {
		return permutation;
	}

	public String getName() {
		return "GreedyDegree";
	}

	
	public void setInput( NGraph<D> g ) {
		graph = g.copy( new MyConvertor() );
	}

	public void run() {
		
		upperBound = Integer.MIN_VALUE;
		while( graph.getNumberOfVertices()>0 ){
			// get vertex with smallest degree
			// TODO make more efficient implementation
			// This can be done by only recomputing the degree of vertices
			// with distance at most 2 from the previously deleted vertex.
			int minDegree = graph.getNumberOfVertices();
			NVertex<GreedyData> smallestVertex = null;
			for( NVertex<GreedyData> v: graph ) {
				if( v.getNumberOfNeighbors() < minDegree){
					minDegree = v.getNumberOfNeighbors();
					smallestVertex = v;
				}
			}
			// add to permutation
			permutation.order.add( smallestVertex.data.original );
			upperBound = Math.max( upperBound, smallestVertex.getNumberOfNeighbors() );		
			// remove from graph
			graph.eliminate( smallestVertex );
		}
	}
	
	public int getUpperBound() {
		return upperBound;
	}
	
	

	
}
