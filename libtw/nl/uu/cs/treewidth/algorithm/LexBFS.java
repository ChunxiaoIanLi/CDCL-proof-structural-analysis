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
import java.util.Collections;
import java.util.Iterator;

import nl.uu.cs.treewidth.input.GraphInput.InputData;
import nl.uu.cs.treewidth.ngraph.NGraph;
import nl.uu.cs.treewidth.ngraph.NVertex;
import nl.uu.cs.treewidth.ngraph.NVertexOrder;

/**
 * Triangulation by using the elimination scheme found by applying 
 * the LEX-P algorithm.
 * These triangulations are not necessarily minimal.
 * 
 * Sourcepaper: A Note on Lexicographic Breadth First Search for
 * Chordal Graphs by Klaus Simon
 *
 * @author team tw
 */
public class LexBFS<D extends InputData> implements Permutation<D> {

	protected NGraph<LBFSData> graph;
	protected NVertexOrder<D> vertexOrder;
	
	
	public NVertexOrder<D> getPermutation() {
		return vertexOrder;
	}

	public String getName() {
		return "Lex-BFS: Lexicographic Breadth First Search";
	}

	
	class LBFSData extends InputData {
		public LBFSData( NVertex<D> old ) { super( old.data.id, old.data.name ); }
		public ArrayList<Integer> labels;
		public boolean visited;
		public int id;
		public NVertex<D> original;
		public NVertex<D> getOriginal() {return original;}
	}
	class MyConvertor implements NGraph.Convertor<D,LBFSData> {
		public LBFSData convert(NVertex<D> old) {
			LBFSData d = new LBFSData(old);
			d.labels = new ArrayList<Integer>();
			d.visited = false;
			d.id = old.data.id;
			d.original = old;
			return d;
		}
	}
	
	
	public void setInput(NGraph<D> g) {
		graph = g.copy( new MyConvertor() );
		vertexOrder = new NVertexOrder<D>();		
	}
	

	/**
	 * Method runs the algorithm and sets the permutation.
	 *
	 */
	public void run() {
		/* forall v in V do label(v) <- EMPTY;
		 * for i<-n downto 1 do
		 * 	let v be an unnumbered vertex with largest label;
		 * 	number(v);
		 * 	forall unnumbered neighbours of v do
		 * 		label(w) <- label(w) + {i}
		 */
		
		
		//for i <- n downto 1 do
		for( int i=graph.getNumberOfVertices(); i>0; --i ){
			NVertex<LBFSData> biggest = null; // Vertex with highest label
			for(int j=0; j<graph.getNumberOfVertices(); ++j) {
				NVertex<LBFSData> v = graph.getVertex(j);
				
				//Only look at vertices that aren't numbered
				if( ! v.data.visited ) {
					
					//Set the first vertex as the init vertex
					if( biggest==null ) {						
						biggest = v;
					} else if( lexBiggerEqual( v.data.labels, biggest.data.labels ) ) {
						biggest = v;						
					}
				
				}
			}
			//Update the neighbours of the selected vertex
			if( biggest!=null ) {
				updateNeigbours(biggest,i);
			}
		}
		Collections.reverse(vertexOrder.order);
	}
	
	
	/*
	 * Update the neigbours; add the roundnumber to their labels
	 * 
	 * @param v the vertex to update
	 * @param round the current round number
	 */
	private void updateNeigbours( NVertex<LBFSData> v, int round) {
		v.data.visited = true;
		vertexOrder.order.add( v.data.getOriginal() );
		
		for( NVertex<LBFSData> other : v ) {
			if( ! other.data.visited ) {
				other.data.labels.add( round );
			}
			
		}
	}
	
	
	/**
	 * Function to compare the labels of the vertices
	 * 
	 * @param a the first ArrayList with integers
	 * @param b the second ArrayList with integers
	 * 
	 * @return if A is bigger or equal then B
	 */
	static boolean lexBiggerEqual( ArrayList<Integer> a, ArrayList<Integer> b ) {
		Iterator<Integer> iA = a.iterator();
		Iterator<Integer> iB = b.iterator();
		while( iA.hasNext() && iB.hasNext() ) {
			int intA = iA.next();
			int intB = iB.next();
			if( intA >= intB ) return true;
			else if( intA < intB ) return false;
		}
		// if a has more, than a is bigger.
		// if a doesn't have more, and b does has more, a is NOT bigger
		//                         and b doesn't have more, they are equal
		return iA.hasNext() ? true : !iB.hasNext();
	}
}
