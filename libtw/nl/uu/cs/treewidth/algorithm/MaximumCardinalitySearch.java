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

import java.util.Collections;

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;
import nl.uu.cs.treewidth.ngraph.NVertexOrder;

/**
 * Triangulation by using the elimination scheme obtained by using 
 * the MCS (Maximum Cardinality Search) algorithm as given by Tarjan and Yannakakis.
 * The triangulation does not need to be minimal.
 * 
 * Reference paper: Maximum Cardinality Search for Computing Minimal Triangulations
 * Anne Berry, Jean R. S. Blair, and Pinar Heggernes
 * 
 * @author tw team 
 */
public class MaximumCardinalitySearch<D extends InputData> implements Permutation<D>, LowerBound<D> {

	protected NGraph<MCSData> graph;
	protected NVertexOrder<D> vertexOrder;
	private int lowerbound = Integer.MIN_VALUE;
	
	public MaximumCardinalitySearch() {
		vertexOrder = new NVertexOrder<D>();
	}
	
	public NVertexOrder<D> getPermutation() {		
		return vertexOrder;
	}

	public String getName() {
		return "MCS; Maximum Cardinality Search Algorithm";
	}

	class MCSData extends InputData {
		public MCSData(NVertex<D> old) { super( old.data.id, old.data.name );}
		int value;
		boolean visited;
		public NVertex<D> original;
		public NVertex<D> getOriginal() {return original;}
		public String toString() {
			String s = super.toString();
			s = s.concat( " (" + value + (visited?"; visited":"")+ ")" );
			return s;
		}
	}
	class MyConvertor implements NGraph.Convertor<D,MCSData> {
		public MCSData convert( NVertex<D> old ) {
			MCSData d = new MCSData( old );
			d.value = 0;
			d.visited = false;
			d.original = old;
			return d;
		}
		
	}
	public void setInput(NGraph<D> g) {
		graph = g.copy(  new MyConvertor() );
	}

	//TODO Make O(n)-implementation
	
	public void run() {
		/*
		 * Algorithm MaximumCardinalitySearch - MCS
		 * Input: A graph G.
		 * Output: An elimination ordering ? of G.
		 * begin
		 * for all vertices v in G do w(v) = 0;
		 * for i = n downto 1 do
		 * 	Choose an unnumbered vertex z of maximum weight; ?(z) = i;
		 * 	for all unnumbered vertices y ? N(z) do w(y) = w(y) + 1;
		 * end
		 */	
		
		//Output.present( graph, "MCS" );
		
		for( int i = graph.getNumberOfVertices()-1; i >= 0; --i ) {
			//Find unnumbered neigbhour with max weight
			int max = 0;
			NVertex<MCSData> z = null;
			for( NVertex<MCSData> v : graph ) {
				if( !v.data.visited && v.data.value>=max ) { 
					z = v;
					max = v.data.value;
				}
			}
			if(z==null)
				continue;
			
			z.data.visited = true;
			vertexOrder.order.add(z.data.getOriginal());
			
			//w(y) = w(y) + 1 for all unnumbered neighbours of z;
			int k = 0;
			for( NVertex<MCSData> other : z ) {
				if( ! other.data.visited ) {
					++other.data.value;					
				} else ++k;
			}
			if( lowerbound < k ) lowerbound = k;
			
			//Output.present( graph, "MCS" );
		}
		Collections.reverse(vertexOrder.order);		
	}

	public int getLowerBound() {
		return lowerbound;
	}

}
