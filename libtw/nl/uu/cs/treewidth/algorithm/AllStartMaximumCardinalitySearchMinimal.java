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
 * Triangulation obtained by using the elimination scheme produced by the MCS (Maximum Cardinality Search) algorithm of Berry et al. 
 * This is a version of MCS that produces minimal triangulations.
 * 
 * Reference paper: Maximum Cardinality Search for Computing Minimal Triangulations
 * Anne Berry, Jean R. S. Blair, and Pinar Heggernes
 * 
 * @author tw team 
 * 
 */
public class AllStartMaximumCardinalitySearchMinimal<D extends InputData> implements Permutation<D>{

	protected NGraph<MCSMData> graph;
	protected NGraph<D> originalGraph;
	private NVertexOrder<D> vertexOrder;
	
	public AllStartMaximumCardinalitySearchMinimal() {
		vertexOrder = new NVertexOrder<D>();
	}
	
	public NVertexOrder<D> getPermutation() {
		return vertexOrder;
	}

	public String getName() {
		return " All Start MCS-M; All Start Maximum Cardinality Search Algorithm Minimal";
	}
	
	
	class MCSMData extends InputData {
		public MCSMData( NVertex<D> old ) {super( old.data.id, old.data.name );}
		int value;
		int dfs;
		boolean visited;
		public NVertex<D> original;
		public NVertex<D> getOriginal() {return original;}
	}
	class MyConvertor implements NGraph.Convertor< D, MCSMData > {
		public MCSMData convert( NVertex<D> old ) {
			MCSMData d = new MCSMData( old );
			d.value = 0;
			d.visited = false;
			d.dfs = Integer.MAX_VALUE;
			d.original = old;
			return d;
		}
	}
	public void setInput( NGraph<D> g ) {
		originalGraph = g;
		graph = g.copy(  new MyConvertor() );
		vertexOrder = new NVertexOrder<D>();
	}

	public void run() {
		/*
		 * F = ?; for all vertices v in G do w(v) = 0;
		 * for i = n downto 1 do
		 * 	Choose an unnumbered vertex z of maximum weight; ?(z) = i;
		 * 	for all unnumbered vertices y ? G do
		 * 		if there is a path y, x1, x2, ..., xk, z in G through unnumbered vertices
		 * 		such that wz?(xi) < wz?(y) for 1 ? i ? k then
		 * 			w(y) = w(y) + 1;
		 * 			F = F ? {yz};
		 * 	H = (V,E ? F);
		 */		
		
		
		int bestUpperBound = Integer.MAX_VALUE;
		for( int startVertex=0; startVertex<graph.getNumberOfVertices(); ++startVertex ){
			
			for(NVertex<MCSMData> v : graph){
				v.data.visited = false;
				v.data.value = 0;
				v.data.dfs = Integer.MAX_VALUE;
			}
			
			NVertexOrder<D> order =  new NVertexOrder<D>();
			
			//Set start vertex
			NVertex<MCSMData> first = graph.getVertex(startVertex);  
			//Update neigbours
			updateVerticesWithPathFrom(first);
			
			//Add first vertex to the permuation
			order.order.add( first.data.getOriginal() );
			for( int i = graph.getNumberOfVertices(); i > 1; --i ) {
			
				//Find unnumbered vertex with max weight
				int max = 0;
				NVertex<MCSMData> z = null;
				for( NVertex<MCSMData> v : graph ) {
					if( !v.data.visited && v.data.value>=max ) {
						z = v;
						max = v.data.value;
					}				
				}
				if(z==null)
					continue;
				z.data.visited = true;
				order.order.add( z.data.getOriginal() );
				
				// Hoog de value van alle unnumbered vertices op, iff, 
				// er een pad van die vertices via andere unnumbered vertices bestaat, 
				// waarbij de vertices op dat pad een lager gewicht hebben.
				
				updateVerticesWithPathFrom(z);
	
			}
			Collections.reverse(order.order);
			// Get the treedecomposition from the given ordering
			PermutationToTreeDecomposition<D> pttd = new PermutationToTreeDecomposition<D>(order);
			pttd.setInput(originalGraph);
			pttd.run();
			int newUpper = pttd.getUpperBound();
			//Compare the new upperbound with the best upperbound so far.
			if( bestUpperBound > newUpper) {
				vertexOrder = order;
				bestUpperBound = newUpper;
			}
		}
	}
	
	public void updateVerticesWithPathFrom(NVertex<MCSMData> z ) {
		for( NVertex<MCSMData> v : graph ) {
			v.data.dfs = Integer.MAX_VALUE;		
		}		
		
		for( NVertex<MCSMData> other : z ) {
			//Kijk alleen naar unnumbered vertices
			if( ! other.data.visited ) {
				//Buren worden zowiezo opgehoogd
				goRecursive( other, other.data.value );
			}
		}
		for( NVertex<MCSMData> other : z ) {
			//Kijk alleen naar unnumbered vertices
			if( ! other.data.visited ) {
				// Buren worden hoe dan ook opgehoogd.
				other.data.dfs = -1;
			}
		}
		
		// Hoog alle vertices met een legaal pad op.
		for( NVertex<MCSMData> v : graph ) {
			if( !v.data.visited ) {
				if( v.data.value > v.data.dfs ) {
					++v.data.value;
				}
			}
		
		}	
	}
	
	
	public void goRecursive( NVertex<MCSMData> v, int w ) {

		if( !v.data.visited && w<v.data.dfs ) {
			v.data.dfs = w;
			for( NVertex<MCSMData> other : v ) {
				int max;
				if( w>v.data.value ) max = v.data.value; else max = w;				
				goRecursive( other, max );
			}
		}		
	}
	
}
