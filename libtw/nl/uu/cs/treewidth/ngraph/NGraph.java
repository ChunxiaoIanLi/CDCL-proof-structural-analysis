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
 
package nl.uu.cs.treewidth.ngraph;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;

import nl.uu.cs.treewidth.output.Output;

public abstract class NGraph< D > implements Iterable<NVertex<D>> {
	
	String comments = "";
	
	public abstract void addVertex( NVertex<D> v );
	public abstract void removeVertex( NVertex<D> v );
	
	public abstract NVertex<D> getVertex( int i );
	public abstract Iterator<NVertex<D>> getVertices();
	public abstract int getNumberOfVertices();
	
	public void addComment( String c ) {
		comments = comments.concat( "\n" + c );
	}

	public String getComments(){
		return comments;
	}
	
	public Iterator<NVertex<D>> iterator() {
		return getVertices();
	}
	
	public void eliminate( NVertex<D> v ) {
		for( NVertex<D> n1 : v ) {
			for( NVertex<D> n2 : v ) {
				if( n1!=n2 ) n1.ensureNeighbor( n2 );
			}
		}
		removeVertex( v );
	}
	public ArrayList<NEdge<D>> eliminate2( NVertex<D> v ) {
		ArrayList<NEdge<D>> es = new ArrayList<NEdge<D>>();
		for( NVertex<D> n1 : v ) {
			for( NVertex<D> n2 : v ) {
				if( n1!=n2 && n1.ensureNeighbor( n2 ) ) {
					es.add( new NEdge<D>(n1,n2) );
				}
			}
		}
		removeVertex( v );
		return es;
	}
	public void deEliminate( NVertex<D> v, ArrayList<NEdge<D>> es ) {
		addVertex( v );
		for( NVertex<D> n : v ) {
			n.ensureNeighbor(v);
		}
		for( NEdge<D> e : es ) {
			e.a.removeNeighbor( e.b );
		}
	}
	
	public void ensureEdge( NVertex<D> a, NVertex<D> b ) {
		a.ensureNeighbor( b );
		b.ensureNeighbor( a );
	}
	public void addEdge( NVertex<D> a, NVertex<D> b ) {
		a.addNeighbor( b );
		b.addNeighbor( a );
	}
	
	public Iterable<NEdge<D>> edges() {
		final NGraph<D> g = this;
		return new Iterable<NEdge<D>>() {
			public Iterator<NEdge<D>> iterator() {
				HashSet<NEdge<D>> edges = new HashSet<NEdge<D>>();
				for( NVertex<D> v : g ) {
					for( NVertex<D> n : v ) {
						edges.add( new NEdge<D>(v,n) );
					}
				}
				return edges.iterator();
			}
			
		};
	}
	
	public int getNumberOfEdges() {
		int n = 0;
		for( NVertex<D> v : this ) {
			n += v.getNumberOfNeighbors();
		}
		return n/2;
	}
	
	public void contractEdge(NEdge<D> e) {
		contractEdge(e.a,e.b);
	}
	
	public void contractEdge(NVertex<D> a, NVertex<D> b) {
		NVertex<D> v1,v2;

		//Select the vertex with the highest degree
		if(a.getNumberOfNeighbors() < b.getNumberOfNeighbors()) {
			v1 = b;
			v2 = a;
		} else {
			v1 = a;
			v2 = b;
		}
		
		//Remove the edge from the edgelists of the vertex
		v1.removeNeighbor(v2);
		v2.removeNeighbor(v1);
		
		//Add vertices of v1 to the list and remove the old edge from those vertices
		for(NVertex<D> ed : v2) {
			
			ensureEdge(v1,ed);
		}
		
		//Remove the other vertex
		removeVertex(v2);	
	}
	
	
	public NVertex<D> getSimplicialVertex() {
		if(getNumberOfVertices()<3)
			return null;
		for( NVertex<D> v : this) {
			if(testSimplicial(v) || testAlmostSimplicial(v))
				return v;
		}
		return null;
	}

	
	/*
	 * A vertex v is simplicial in an undirected
	 * graph G if the neighbours of v form a clique in G.
	 */
	public boolean testSimplicial(NVertex<D> v) {
		for(NVertex<D> neighbor1: v) {
			for(NVertex<D> neighbor2: v) {
				if(neighbor1.data != neighbor2.data)
					if(!neighbor1.isNeighbor(neighbor2))
						return false;				
			}
		}
		return true;
	}
	
	
	/*
	 * A vertex v is almost simplicial in an undirected graph G 
	 * if there is a neighbour w of v such that all other neighbours of v form a clique in G.
	 * TODO: controleren of dit goed werkt!
	 */
	public boolean testAlmostSimplicial(NVertex<D> v) {
		for(NVertex<D> uberv: v) {
			for(NVertex<D> neighbor1: v) {
				for(NVertex<D> neighbor2: v) {
					if(neighbor1.data != neighbor2.data && neighbor1.data!=uberv.data && neighbor2.data!=uberv.data)
						if(!neighbor1.isNeighbor(neighbor2))
							return false;				
				}
			}
		}
		return true;
	}
	
	public abstract void setVertices( ArrayList<NVertex<D>> vs );
	
	public static interface Convertor< From, To > {
		public To convert( NVertex<From> v );
	}
	public <To> NGraph<To> copy( Convertor<D,To> c ) {
				
		NGraph<To> newG = new ListGraph<To>();
		
		HashMap<NVertex<D>, NVertex<To>> oldToNew = new HashMap<NVertex<D>, NVertex<To>>();
		
		for( NVertex<D> v : this ) {
			To newData = c.convert( v );
			NVertex<To> nv = v.newOfSameType( newData );
			newG.addVertex( nv );
			oldToNew.put( v, nv );
		}
		for( NVertex<D> v : this ) {
			for( NVertex<D> n : v ) {
				oldToNew.get(v).addNeighbor(oldToNew.get(n));
			}
		}
		
		return newG;
		
	}
	
	public NGraph<D> copy() {
		
		NGraph<D> newG = new ListGraph<D>();
		
		HashMap<NVertex<D>, NVertex<D>> oldToNew = new HashMap<NVertex<D>, NVertex<D>>();
		
		for( NVertex<D> v : this ) {
			NVertex<D> nv = v.newOfSameType( v.data );
			newG.addVertex( nv );
			oldToNew.put( v, nv );
		}
		for( NVertex<D> v : this ) {
			for( NVertex<D> n : v ) {
				oldToNew.get(v).addNeighbor(oldToNew.get(n));
			}
		}
		
		return newG;
		
	}
		
	public void printGraph(boolean toWindow, boolean toFile) {
		Output.toWindow = toWindow;
		Output.toFile = toFile;
		Output.present(this,"");
	}
	
}
