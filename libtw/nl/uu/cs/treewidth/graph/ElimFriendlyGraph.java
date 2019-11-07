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
 
package nl.uu.cs.treewidth.graph;

import java.util.ArrayList;

import nl.uu.cs.treewidth.input.GraphInput.InputData;


/**
 * <p><emph>Deprecated! Use the NGraph instead.</emph></p>
 * But it <emph>would</emph> be interesting to do
 * an adjacency matrix implementation for the NGraph, or even this funky piece of integer
 * twiddling.
 * 
 * @author tw team
 *
 */
@Deprecated
public class ElimFriendlyGraph< Data > {

	int n;
	int[][] matrix;
	int[] start;
	int[] degree;
	Object[] data;
	boolean[] eliminated;
	
	public ElimFriendlyGraph( int n ) {
		init( n );
	}
	public ElimFriendlyGraph( Graph<? extends InputData> g ) {
		// first init
		int size = g.vertices.size();
		init( size );
		
		for( int i=0; i<size; ++i ) {
			Vertex<? extends InputData> v = g.vertices.get(i);			
			// copy the edges
			initVertex( v );
		}
	}
	
	protected void init( int n ) {
		// size of the graph
		this.n = n;
		
		// adjacency matrix with embedded edge lists
		// forall v. matrix[v][0] is unused.
		// {more description}
		matrix = new int[n+1][n+1];
		// all elements start out at zero.
		
		// keep track of the `start' of the edge list
		start = new int[n+1];
		// all list are empty: their `end' is zero.
		
		// keep track of the degree of the vertices
		degree = new int[n+1];
		// the graph start out empty, so all zeroes.
		
		// remember arbitrary data at vertices
		data = new Object[n+1];
		
		// no vertices have been eliminated yet
		eliminated = new boolean[n+1];
		
	}
	
	public void initVertex( Vertex<? extends InputData> v ) {
		int id = v.data.id+1; // InputData's id starts at zero, we at one.
		for( Edge<? extends InputData> e : v.edges ) {
			ensureEdge( id, e.a==v? e.b.data.id+1 : e.a.data.id+1);
		}
	}
	
	public boolean edgeExists( int v1, int v2 ) {
		return matrix[v1][v2]>0;
	}
	
	public void ensureEdge( int v1, int v2 ) {
		
		if( matrix[v1][v2] == 0 ) { // there is currently no edge
			
			// add the edge to this vertex; it is the new start of
			// the list, so let it point to the old start.
			// if there was no start yet, you are the end of the list
			int next = start[v1];
			matrix[v1][v2] = next==0? v2 : next;
			
			// remember that this is the new start of the list
			start[v1] = v2;
			
			// v1's degree is up by one
			++degree[v1];
		
		} else if( matrix[v1][v2] < 0 ) { // there is a forwarding address.
			// fine! just turn it back on.
			matrix[v1][v2] = -matrix[v1][v2];
			
		} // else there already was an edge
		
	}
	
	public void removeEdge( int v1, int v2 ) {
		
		if( matrix[v1][v2] > 0 ) { // there currently is an edge
			
			// indicate this edge no longer exists, but do leave
			// a forwarding address so we don't break the list
			matrix[v1][v2] = -matrix[v1][v2];
			
			// v1's degree is down by one
			--degree[v1];
			
		} // else there was no edge to begin with
		
	}
	
	public int degree( int v ) {
		return degree[v];
	}
	
	public int getNeighbours_( int v, /*out*/ int N[] ) {
		
		int numN = 0;
		
		//print();
		
		if( start[v] == 0 ) {
			// there is no edge list, so the degree had better be zero
			assert( degree[v]==0 );
			return 0;
		}
		
		// just walk the edge list and clean up any forwarding addresses
		int i = start[v];
		int prev = i;
		boolean done = false;
		while( !done ) {
			int next = matrix[v][i];
			
			if( next<0 ) {
				// not a real edge, just a forwarding address
				
				// translate to real address
				next = -next;

				if( next==i ) {
					// end of the list: fix the previous element
					// to be the end of the list
					if( start[v]==i ) {
						assert( false ); // cannot be both the start and the end of a non-empty list and not exist
					} else {
						// not start of list, so prev is valid.
						matrix[v][prev] = prev;
					}
					// end of list
					done = true;
				} else {
					if( start[v]==i ) {
						// start of list.
						// not end of list, so next is valid
						start[v] = next;
					} else {
						matrix[v][prev] = next;
					}
				}
				
				// forward handled, clean this cell
				matrix[v][i] = 0;
				
				// don't update prev, because this is not real anymore; it is 0.
				
				
			} else if( next>0 ) {
				// a real edge
				
				N[numN++] = i;
				
				if( next==i ) {
					// end of list
					done = true;
				}
				
				prev = i;
				
			} else assert( false ); // next should never be zero.

			i = next;
		}
		
		return degree[v];
	}
	
	public int[] getNeighbours( int v ) {
		int[] N = new int[degree[v]];
		getNeighbours_( v, N );
		return N;		
	}
	
	public void eliminate( int v ) {
		int[] N = getNeighbours(v);
		int len = N.length;
		for( int outer=0; outer<len; ++outer ) {
			//removeEdge( v, N[outer] ); // also throw away the edges of the eliminated vertex?
			removeEdge( N[outer], v );
			for( int inner=outer+1; inner<len; ++inner ) {
				ensureEdge( N[inner], N[outer] );
				ensureEdge( N[outer], N[inner] );
			}
		}
		eliminated[v] = true;
	}
	
	public boolean isEliminated( int v ) {
		return eliminated[v];
	}
	
	/**
	 * Beware: pretty nasty performance. To be used when you know there are little live vertices.
	 */
	public ArrayList<Integer> getNonEliminatedVertices() {
		ArrayList<Integer> vs = new ArrayList<Integer>();
		for( int i=1; i<=n; ++i ) {
			if( !eliminated[i] ) vs.add(i);
		}
		return vs;
	}
	
	public void print() {
		for( int v=1; v<=n; ++v ) {
			System.out.print( "[" + start[v] + "]\t" );
			for( int e=1; e<=n; ++e ) {
				System.out.print( matrix[v][e] + "\t" );
			}
			System.out.println();
		}
		System.out.println();
	}
	
	public void setData( int v, Data d ) {
		data[v] = d;
	}
	@SuppressWarnings("unchecked")
	public Data getData( int v ) {
		return (Data)data[v];
	}
	
	public int size() {
		return n;
	}

}
