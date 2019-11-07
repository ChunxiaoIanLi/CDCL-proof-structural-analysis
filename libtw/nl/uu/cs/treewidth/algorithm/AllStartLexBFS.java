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
 * This All Start Version is run n times; everytime selecting a different vertex to start with. 
 * 
 * Sourcepaper: A Note on Lexicographic Breadth First Search for
 * Chordal Graphs by Klaus Simon
 *
 * @author team tw
 */
public class AllStartLexBFS < D extends InputData > implements Permutation<D>, UpperBound<D> {

	protected NGraph<LBFSData> graph;
	protected NGraph<D> originalGraph;
	protected NVertexOrder<D> vertexOrder;
	protected int upperbound;
	
	public NVertexOrder<D> getPermutation() {
		return vertexOrder;
	}

	public String getName() {
		return "All Start Lex-BFS: All Start Lexicographic Breadth First Search";
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
	
	
	/**
	 * @param g the input graph  
	 */
	public void setInput(NGraph<D> g) {
		originalGraph = g;
		graph = g.copy( new MyConvertor() );
		vertexOrder = new NVertexOrder<D>();
		upperbound = Integer.MAX_VALUE;
	}

	
	/**
	 * Method runs the algorithm and sets the permutation.
	 *
	 */
	public void run() {
		/* forall v in V doe label(v) <- EMPTY;
		 * for i<-n downto 1 do
		 * 	let v be an unnumbered vertex with largest label;
		 * 	number(v);
		 * 	forall unnumbered neighbours of v do
		 * 		label(w) <- label(w) + {i}
		 */
		NVertexOrder<D> order =  new NVertexOrder<D>();
		int bestUpperBound = Integer.MAX_VALUE;
		for( int startVertex=0; startVertex<graph.getNumberOfVertices(); ++startVertex ){
			for(NVertex<LBFSData> v : graph){
				v.data.visited = false;
				v.data.labels.clear();
				order.order.clear();
			}
			
			//Set start vertex
			NVertex<LBFSData> first = graph.getVertex(startVertex);
			//Update his neigbours
			updateNeigbours(first, graph.getNumberOfVertices() );
			//Add the first vertex to the permutation
			order.order.add( first.data.getOriginal() );
			
			//for i <- n downto 1 do
			for( int i=graph.getNumberOfVertices()-1; i>0; --i ){
				NVertex<LBFSData> biggest = null; // Vertex with highest label
				for(int j=0; j<graph.getNumberOfVertices(); ++j) {
					NVertex<LBFSData> v = graph.getVertex(j);					
					//Only look at vertices that aren't numbered
					if( ! v.data.visited ) {						
						//Set the first vertex as the init vertex
						if( biggest==null ) {						
							biggest = v;
						} else if( lexBigger( v.data.labels, biggest.data.labels ) ) {
							biggest = v;						
						}					
					}
				}
				//Update the neighbours of the selected vertex
				if( biggest!=null ) {
					updateNeigbours(biggest, i );
					order.order.add( biggest.data.getOriginal() );					
				}
			}
			//Reverse the list
			Collections.reverse(order.order);
			
			//Create the treedecomposition to get the upperbound 
			PermutationToTreeDecomposition<D> pttd = new PermutationToTreeDecomposition<D>(order);
			pttd.setInput(originalGraph);
			pttd.run();
			int newUpper = pttd.getUpperBound();
			if( bestUpperBound > newUpper) {
				vertexOrder = new NVertexOrder<D>(order);
				bestUpperBound = newUpper;				
			}
		}
		upperbound = bestUpperBound;
	}
	
	
	/*
	 * Function to recursively select all the vertices that have lowest labels
	 * 
	 * This function isnt used anymore, cause branching was only effective the first round.
	 */
	@SuppressWarnings("unused")
	private void goRecursive(NGraph<LBFSData> g, int round, NVertexOrder<D> order) {
		//Laatste ronde!
		if( order.order.size() == g.getNumberOfVertices() ) {
			//Reverse the list
			Collections.reverse(order.order);
			
			//Create the treedecomposition to get the upperbound 
			PermutationToTreeDecomposition<D> pttd = new PermutationToTreeDecomposition<D>(order);
			pttd.setInput(originalGraph);
			pttd.run();
			int newUpper = pttd.getUpperBound();
			if( upperbound > newUpper) {
				vertexOrder = new NVertexOrder<D>(order);
				upperbound = newUpper;				
			}
			//Reverse the list
			Collections.reverse(order.order);
		} else {		
		
			//Lijst waarin alle vertices staan waar we recursief op gaan
			ArrayList <NVertex<LBFSData>> biggest = new ArrayList<NVertex<LBFSData>>(); 
			
			//Zoek de vertices met grootste labels
			for(int j=0; j<g.getNumberOfVertices(); ++j) {
				NVertex<LBFSData> v = g.getVertex(j);
				
				//Only look at vertices that aren't numbered
				if( ! v.data.visited ) {
					
					//Set the first vertex as the init vertex
					if( biggest.size()==0 ) {						
						biggest.add(v);
					} else if( lexEqual( v.data.labels, biggest.get(0).data.labels ) ) {
						biggest.add(v);						
					}else if( lexBigger( v.data.labels, biggest.get(0).data.labels ) ) {
						biggest.clear();
						biggest.add(v);						
					}		
				}
			}
			int nextRound = round-1;
			
			//If you do not want to branch on all the items, set a tiebreak here.
			if(biggest.size()<=g.getNumberOfVertices()-1) {
				//int randIndex = (int)(Math.random() * biggest.size());
				int randIndex = biggest.size()-1;
				NVertex<LBFSData> v = biggest.get(randIndex);
				//Update buren en stop vertices in de lijst
				updateNeigbours(v, round );
				order.order.add( v.data.getOriginal() );
				
				goRecursive(g,nextRound,order);
				
				//Undo update buren en verwijder vertices uit de lijst.
				order.order.remove(v.data.getOriginal());
				reverseUpdateNeigbours(v,round);
			} else {
				for(NVertex<LBFSData> v : biggest) {
					//Update buren en stop vertices in de lijst
					updateNeigbours(v, round );
					order.order.add( v.data.getOriginal() );
					
					goRecursive(g,nextRound,order);
					
					//Undo update buren en verwijder vertices uit de lijst.
					order.order.remove(v.data.getOriginal());
					reverseUpdateNeigbours(v,round);
				}
			}
		}		
	}
	
	/*
	 * Update the neigbours; add the roundnumber to their labels
	 */
	private void updateNeigbours( NVertex<LBFSData> v, Integer round) {
		v.data.visited = true;		
		for( NVertex<LBFSData> other : v ) {
			if( ! other.data.visited ) {
				other.data.labels.add( round );
			}			
		}
	}
	
	/*
	 * Update the neigbours; add the roundnumber to their labels
	 */
	private void reverseUpdateNeigbours( NVertex<LBFSData> v, Integer round) {
		v.data.visited = false;		
		for( NVertex<LBFSData> other : v ) {
			if( ! other.data.visited ) {
				other.data.labels.remove( round );				
			}			
		}
	}
	
	
	/**
	 * Function to compare the labels of the vertices
	 * 
	 * @param a the first ArrayList with integers
	 * @param b the second ArrayList with integers
	 * 
	 * @return if A is bigger then B
	 */
	static boolean lexBigger( ArrayList<Integer> a, ArrayList<Integer> b ) {
		Iterator<Integer> iA = a.iterator();
		Iterator<Integer> iB = b.iterator();
		while( iA.hasNext() && iB.hasNext() ) {
			int intA = iA.next();
			int intB = iB.next();
			if( intA > intB ) return true;
			else if( intA < intB ) return false;
		}
		// if a has more, than a is bigger.
		// if a doesn't have more, and b does has more, a is NOT bigger
		//                         and b doesn't have more, they are equal
		return iA.hasNext() ? true : !iB.hasNext();
	}
	
	
	/**
	 * Function to compare the labels of the vertices
	 * 
	 * @param a the first ArrayList with integers
	 * @param b the second ArrayList with integers
	 * 
	 * @return if A is equal to B
	 */
	static boolean lexEqual( ArrayList<Integer> a, ArrayList<Integer> b ) {
		Iterator<Integer> iA = a.iterator();
		Iterator<Integer> iB = b.iterator();
		while( iA.hasNext() && iB.hasNext() ) {
			int intA = iA.next();
			int intB = iB.next();
			if( intA > intB ) return false;
			else if( intA < intB ) return false;
		}
		if(iA.hasNext() || iB.hasNext())
			return false;
		else
			return true;		
	}

	
	/**
	 * @return the upperbound
	 */
	public int getUpperBound() {
		return upperbound;
	}
}
