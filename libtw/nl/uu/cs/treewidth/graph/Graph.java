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
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;

/**
 * <p><emph>Deprecated! Use the NGraph instead.</emph></p>
 * <p>Standard datastructure for representing graphs. Its main use is as
 * a standardized way to communicate graphs throughout the framework.
 * (For example, a <code>GraphInput</code> returns a Graph and an <code>
 * Algorithm</code> gets its input as a Graph.)</p>
 * 
 * <p>TODO More explanation of how the datastructure works.</p>
 * 
 * 
 * 
 * <p>
 * <i>Example usage:</i> Read a graph from a file in DGF format.
 * </p>
 * <pre>
 * GraphInput input = new DgfReader( "myGraph.dgf" );
 * Graph g = new Graph();
 * try {
 * 
 *     g = input.get();
 *     
 * } catch (InputException e) { ... }
 * </pre>
 *  
 * 
 * 
 * <p>
 * <i>Example usage:</i> Manually create C<sub>3</sub>
 * </p>
 * <pre>
 * Graph g = new Graph();
 * 
 * Vertex v1 = new Vertex();
 * g.addVertex( v1 );
 * 
 * Vertex v2 = new Vertex();
 * g.addVertex( v2 );
 * 
 * Vertex v3 = new Vertex();
 * g.addVertex( v3 );
 * 
 * g.addEdge( v1, v2 );
 * g.addEdge( v2, v3 );
 * g.addEdge( v3, v1 );
 * </pre>
 * 
 * @author tw team
 * @param <Data> 
 *
 */
@Deprecated
public class Graph< Data > {

	String comments;
	private ArrayList<Edge<Data>> edges;
	private boolean edgeChanged;
	
	/**
	 * List of the vertices of the graph.
	 */
	public ArrayList<Vertex<Data>> vertices;
	
	/**
	 * Creates an empty graph with no comments.
	 */
	public Graph() {
		comments = "";
		vertices = new ArrayList<Vertex<Data>>();
		edgeChanged = true;
	}
	

	/**
	 * Adds a vertex to the graph.
	 * 
	 * @param v The vertex to add.
	 */
	public void addVertex( Vertex<Data> v ) {
		vertices.add( v );
		edgeChanged = true;
	}
	
	/**
	 * Adds an edge between a and b in the graph.
	 * 
	 * @param a
	 * @param b
	 */
	public void addEdge( Vertex<Data> a, Vertex<Data> b ) {
		Edge<Data> e = new Edge<Data>( a, b );
		a.edges.add( e );
		b.edges.add( e );
		
		edgeChanged = true;
	}
	
	/**
	 * Adds a new line of comments to the graph. (Note that a newline is automatically prefixed.)
	 * 
	 * @param c The comment line
	 */
	public void addComment( String c ) {
		comments = comments + "\n" + c;
	}
	
	/**
	 * @return The comments for this graph.
	 */
	public String getComments() {
		return comments;
	}
	
	/**
	 * Computes the edgelist of the graph.<br/>
	 * <b>Caution:</b> This method uses cached data. If you manually change the vertices in the graph, call the function clearEdgeCache() to make sure the cached data is not used.
	 * 
	 * @return Edgelist of the graph.
	 */
	public ArrayList<Edge<Data>> getEdges(){
		//if (edgeChanged){
			HashSet<Vertex<Data>> visited = new HashSet<Vertex<Data>>();
			ArrayList<Edge<Data>> newEdges = new ArrayList<Edge<Data>>();
			for (Vertex<Data> v: vertices){
				for (Edge<Data> e: v.edges){
					if (!visited.contains(e.other(v))){
						newEdges.add(e);
					}
				}
				visited.add(v);
			}
			edges = newEdges;
			edgeChanged = false;
		//}
		return edges;
	}
	
	
	public static interface Convertor< OldData, NewData > {
		NewData convert( Vertex<? extends OldData> old );
	}
	
	/**
	 * Does <i>NOT</i> make a deep copy of the vertices' data.
	 * 
	 * @author tw team
	 *
	 * @param <CopiedData>
	 */
	public static class Copier<CopiedData> implements Convertor<CopiedData,CopiedData> {
		public CopiedData convert(Vertex<? extends CopiedData> old) {
			return old.data;
		}	
	}
	
	public static <CopiedData> Graph<CopiedData> shallowCopy( Graph<CopiedData> g ){
		return copy(g,new Copier<CopiedData>());
	}
	
	public static < OldData, NewData > Graph<NewData> copy( Graph<? extends OldData> oldG, Convertor<OldData,NewData> dataConvertor ) {

		// The new graph 
		Graph<NewData> newG = new Graph<NewData>();
		
		// Convert the vertices; build a translation table
		HashMap<Vertex<? extends OldData>,Vertex<NewData>> oldToNewVertex = new HashMap<Vertex<? extends OldData>,Vertex<NewData>>();
		for( Vertex<? extends OldData> oldVertex : oldG.vertices ) {
			// Create a new vertex from the old one
			Vertex<NewData> newVertex = new Vertex<NewData>();
			newVertex.data = dataConvertor.convert( oldVertex );
			oldToNewVertex.put( oldVertex, newVertex );
			newG.addVertex( newVertex );
		}
		
		// now translate all the edges.
		for( Edge<? extends OldData> e : oldG.getEdges() ) {
			Vertex<NewData> newA = oldToNewVertex.get(e.a);
			Vertex<NewData> newB = oldToNewVertex.get(e.b);
			newG.addEdge( newA, newB );
		}
		
		// done!
		return newG;
		
	}
	
	public void contractEdge(Edge<Data> e){
		
		//Select the vertex with the highest degree
		Vertex<Data> v1,v2;
		
		if(e.a.edges.size() < e.b.edges.size())
			v1 = e.b;
		else
			v1 = e.a;
		
		//The vertex we are going to remove
		v2 = e.other(v1);
		
		//Remove the edge from the edgelists of the vertex
		v1.edges.remove(e);
		v2.edges.remove(e);
		
		//Add vertices of v1 to the list and remove the old edge from those vertices
		for(Edge<Data> ed : v2.edges) {
			ensureEdge(v1,ed.other(v2));
			//ed.other(v2).edges.remove(ed);
		}
		
		//Remove the other vertex
		removeVertex(v2);
		
	}
	
	public void removeVertex( Vertex<Data> v) {
		for( Edge<Data> e : v.edges) {
			e.other(v).edges.remove(e);
		}
		vertices.remove(v);
		edgeChanged = true;
	}
	
	/**
	 * Eliminates a vertex from the copy of the graph by marrying the neighbors and removing the vertex.<br/>
	 * This method does <b>NOT</b> update the edgelist of the copy of the graph, because it is not used.
	 * 
	 * Returns a list with edges added during the elimination proces
	 * 
	 * @param v The vertex to remove from the copy of the graph.
	 */
	@SuppressWarnings("unchecked")
	public <T> ArrayList<Edge<T>> eliminateVertex(Vertex<T> v){
		LinkedList<Vertex<T>> neighbors = new LinkedList<Vertex<T>>();
		ArrayList<Edge<T>> newEdges = new ArrayList<Edge<T>>(); 
		for (Edge<T> e: v.edges){
			Vertex<T> other = e.other(v);
			if (!other.edges.remove(e)){
				System.out.println("Borked, did not remove edge.");
			}
			for(Vertex<T> n: neighbors){
				Edge<T> newEdge = ensureEdge(other,n);
				if(newEdge!=null)
					newEdges.add(newEdge);
			}
			neighbors.add(other);
		}
		vertices.remove(v);
		edgeChanged = true;
		return newEdges;
	}
	
	/**
	 * Function adds a vertex and removes edges; it reverses a vertex elimination
	 */
	public void deEliminateVertex(Vertex<Data> v, ArrayList<Edge<Data>> addedEdges) {
		//Voeg vertex weer toe
		addVertex(v);
		for(Edge<Data> e : v.edges) {
			e.other(v).edges.add(e);			
		}
		
		//Verwijder toegevoegde edges
		for(Edge<Data> e : addedEdges) {
			removeEdge(e);
		}
		edgeChanged = true;
	}
	
	
	
	/**
	 * 
	 * TODO Make more efficient implementation.
	 * 
	 * Ensures that an edge is present between two vertices.<br/>
	 * This method does <b>NOT</b> update the edgelist of the copy of the graph, because it is not used.
	 * 
	 * @param v1 First vertex of the edge.
	 * @param v2 Second vertex of the edge.
	 */
	private <T> Edge ensureEdge(Vertex<T> v1, Vertex<T> v2){
		boolean present = false;
		for (Edge<T> e: v1.edges){		
			Vertex<T> other = e.other(v1);
			if (other == v2) {
				present = true;
				break;
			}		
		}
		Edge<T> edge = null;
		if (!present){
			edge = new Edge<T>(v1,v2);
			v1.edges.add(edge);
			v2.edges.add(edge);
		}
		edgeChanged = true;
		return edge;
	}
	
	/**
	 * Removes an edge from the edgelist of it's two vertices
	 */
	public void removeEdge(Edge<Data> e) {
		e.a.edges.remove(e);
		e.b.edges.remove(e);
	}
	
	
	/**
	 * Makes sure the cached edgelist is no longer used. Call this function if you change something in the vertices of the graph without using the methods in Graph. 
	 */
	public void clearEdgeCache(){
		edgeChanged = true;
	}

	public Graph( NeighborHashSetGraph<Data> g ) {
		comments = "";
		vertices = new ArrayList<Vertex<Data>>();
		edgeChanged = true;
		
		// Convert the vertices; build a translation table
		HashMap<NeighborHashSetVertex<Data>,Vertex<Data>> oldToNewVertex = new HashMap<NeighborHashSetVertex<Data>,Vertex<Data>>();
		for( NeighborHashSetVertex<Data> oldVertex : g.vertices ) {
			// Create a new vertex from the old one
			Vertex<Data> newVertex = new Vertex<Data>();
			newVertex.data = oldVertex.data;
			oldToNewVertex.put( oldVertex, newVertex );
			addVertex( newVertex );
		}
		
		// now translate all the edges.
		for( NeighborHashSetEdge<Data> e : g.getEdges() ) {
			Vertex<Data> newA = oldToNewVertex.get(e.a);
			Vertex<Data> newB = oldToNewVertex.get(e.b);
			addEdge( newA, newB );
		}
		
		// done!
	}
	
}
