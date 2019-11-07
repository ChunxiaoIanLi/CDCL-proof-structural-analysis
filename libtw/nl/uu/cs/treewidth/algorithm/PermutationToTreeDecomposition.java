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
import nl.uu.cs.treewidth.ngraph.ListGraph;
import nl.uu.cs.treewidth.ngraph.ListVertex;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NTDBag;
import nl.uu.cs.treewidth.ngraph.NVertex;
import nl.uu.cs.treewidth.ngraph.NVertexOrder;

public class PermutationToTreeDecomposition<D extends InputData> implements UpperBound<D>, Constructive<D> {

	private Permutation<D> permAlg;
	private int upperBound;
	private NGraph<PermutedData> gcopy;
	private NVertex[] original2copy;
	private NGraph<NTDBag<D>> decomp;
	private NVertexOrder<D> givenPermutation;
	
	class PermutedData {
		int permIndex;
		NVertex<NTDBag<D>> bag;
		NVertex<D> original;
		public PermutedData(NVertex<D> old) { original = old; }
	}
	class Convertor implements NGraph.Convertor<D,PermutedData> {
		public PermutedData convert( NVertex<D> old ) {
			PermutedData d = new PermutedData( old );
			return d;
		}
	}
	
	/**
	 * Create an instance of the PermutationToTreeDecomposition algorithm and
	 * use a Permutation algorithm to get the permutation.
	 * @param permAlg The Permutation algorithm to use.
	 */
	public PermutationToTreeDecomposition(Permutation<D> permAlg){
		this.permAlg = permAlg;
	}
	
	/**
	 * Create an instance of the PermutationToTreeDecomposition algorithm and
	 * use a given permutation.
	 * @param givenPermutation The permutation to use.
	 */
	public PermutationToTreeDecomposition(NVertexOrder<D> givenPermutation){
		this.givenPermutation = givenPermutation;
	}
	
	public int getUpperBound() {
		return upperBound;
	}

	public String getName() {
		if( permAlg!=null )
			return "Permutation To Tree Decomposition with " + permAlg.getName();
		else
			return "Permutation To Tree Decomposition";
	}

	public void setInput(NGraph<D> g) {
		if( permAlg!=null ) permAlg.setInput(g);
		gcopy = g.copy( new Convertor() );
		original2copy = new NVertex[gcopy.getNumberOfVertices()];
		for (NVertex<PermutedData> v: gcopy){
			original2copy[v.data.original.data.id] = v;
		}
	}

	@SuppressWarnings("unchecked")
	public void run() {
		NVertexOrder<D> permutation;
		if( givenPermutation != null ) permutation = givenPermutation;
		else {
			permAlg.run();
			permutation = permAlg.getPermutation();
		}
		int i = 0;
		for (NVertex<D> v: permutation.order){
			NVertex<PermutedData> vp = (NVertex<PermutedData>) original2copy[v.data.id];
			vp.data.permIndex = i;
			++i;
		}
		decomp = new ListGraph<NTDBag<D>>();
		//upperBound = permWidth(permutation);
		permDecomp(permutation,0);
	}
	
	/**
	 * Calculates the treewith and builds a tree decomposition of the input graph when using the given permutation.
	 * 
	 * @param g Input Graph to run on.
	 * @param permutation Permutation to eliminate the vertices in the input graph.
	 * @return Tree decomposition of the input graph given the elimination ordering.
	 */
	@SuppressWarnings("unchecked")
	private void permDecomp(NVertexOrder<D> permutation, int permIndex){
		int size = gcopy.getNumberOfVertices();
		if (size == 0){
			upperBound = Integer.MIN_VALUE;
		} else if (size == 1){
			upperBound = 0;
			NTDBag<D> bag = new NTDBag<D>();
			bag.vertices.add( gcopy.getVertex(0).data.original );
			decomp.addVertex(new ListVertex<NTDBag<D>>(bag));
		} else if (size == 2){
			upperBound = 1;
			NTDBag<D> bag = new NTDBag<D>();
			bag.vertices.add( gcopy.getVertex(0).data.original );
			bag.vertices.add( gcopy.getVertex(1).data.original );
			NVertex<NTDBag<D>> decompVertex = new ListVertex<NTDBag<D>>(bag);
			decomp.addVertex(decompVertex);
			gcopy.getVertex(0).data.bag = decompVertex;
			gcopy.getVertex(1).data.bag = decompVertex;
		} else {
			NVertex<PermutedData> thisVertex = original2copy[permutation.order.get(permIndex).data.id];
			gcopy.eliminate(thisVertex);
			//go into recursion
			permDecomp(permutation, permIndex+1);
			//create a bag and add it to the decomposition
			int numNeighbors = thisVertex.getNumberOfNeighbors();
			NTDBag<D> bag = new NTDBag<D>();
			int lowestIndex = Integer.MAX_VALUE;
			NVertex<PermutedData> lowestNeighbor = null;
			bag.vertices.add(thisVertex.data.original);
			for (NVertex<PermutedData> other: thisVertex){
				bag.vertices.add(other.data.original);
				if (other.data.permIndex < lowestIndex){
					lowestIndex = other.data.permIndex;
					lowestNeighbor = other;
				}
			}
			NVertex<NTDBag<D>> decompVertex = new ListVertex<NTDBag<D>>(bag);
			decomp.addVertex(decompVertex);
			thisVertex.data.bag = decompVertex;
			//create an edge between the bag and the neighborhoodbag
			if(lowestNeighbor != null)
				decomp.addEdge(decompVertex,lowestNeighbor.data.bag);
			//calculate the upperbound
			upperBound = Math.max(numNeighbors, upperBound);
		}
	}
	
	public NGraph<NTDBag<D>> getDecomposition() {
		return decomp;
	}

}
