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
public class NeighborHashSetGraph< Data > {

	String comments;
	private ArrayList<NeighborHashSetEdge<Data>> edges;
	private boolean edgeChanged;
	public Graph<Data> original;
	
	/**
	 * List of the vertices of the graph.
	 */
	public ArrayList<NeighborHashSetVertex<Data>> vertices;
	
	/**
	 * Creates an empty graph with no comments.
	 */
	public NeighborHashSetGraph() {
		comments = "";
		vertices = new ArrayList<NeighborHashSetVertex<Data>>();
		edgeChanged = true;
	}
	
	public NeighborHashSetGraph( Graph<Data> g ) {
		original = g;
		comments = "";
		vertices = new ArrayList<NeighborHashSetVertex<Data>>();
		edgeChanged = true;
		
		// Convert the vertices; build a translation table
		HashMap<Vertex<Data>,NeighborHashSetVertex<Data>> oldToNewVertex = new HashMap<Vertex<Data>,NeighborHashSetVertex<Data>>();
		for( Vertex<Data> oldVertex : g.vertices ) {
			// Create a new vertex from the old one
			NeighborHashSetVertex<Data> newVertex = new NeighborHashSetVertex<Data>();
			newVertex.data = oldVertex.data;
			oldToNewVertex.put( oldVertex, newVertex );
			addVertex( newVertex );
		}
		
		// now translate all the edges.
		for( Edge<Data> e : g.getEdges() ) {
			NeighborHashSetVertex<Data> newA = oldToNewVertex.get(e.a);
			NeighborHashSetVertex<Data> newB = oldToNewVertex.get(e.b);
			addEdge( newA, newB );
		}
		
		// done!
	}
	
	public <OldData> NeighborHashSetGraph( Graph<? extends OldData> g, Graph.Convertor<OldData,Data> dataConvertor ) {
		comments = "";
		vertices = new ArrayList<NeighborHashSetVertex<Data>>();
		edgeChanged = true;
		
		// Convert the vertices; build a translation table
		HashMap<Vertex<? extends OldData>,NeighborHashSetVertex<Data>> oldToNewVertex = new HashMap<Vertex<? extends OldData>,NeighborHashSetVertex<Data>>();
		for( Vertex<? extends OldData> oldVertex : g.vertices ) {
			// Create a new vertex from the old one
			NeighborHashSetVertex<Data> newVertex = new NeighborHashSetVertex<Data>();
			newVertex.data = dataConvertor.convert(oldVertex);
			oldToNewVertex.put( oldVertex, newVertex );
			addVertex( newVertex );
		}
		
		// now translate all the edges.
		for( Edge<? extends OldData> e : g.getEdges() ) {
			NeighborHashSetVertex<Data> newA = oldToNewVertex.get(e.a);
			NeighborHashSetVertex<Data> newB = oldToNewVertex.get(e.b);
			addEdge( newA, newB );
		}
		
		// done!
	}
	
	/**
	 * Adds a vertex to the graph.
	 * 
	 * @param v The vertex to add.
	 */
	public void addVertex( NeighborHashSetVertex<Data> v ) {
		vertices.add( v );
		edgeChanged = true;
	}
	
	/**
	 * Adds an edge between a and b in the graph.
	 * 
	 * @param a
	 * @param b
	 */
	public void addEdge( NeighborHashSetVertex<Data> a, NeighborHashSetVertex<Data> b ) {
		a.neighbors.add(b);
		b.neighbors.add(a);
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
	public ArrayList<NeighborHashSetEdge<Data>> getEdges(){
		if (edgeChanged){
			HashSet<NeighborHashSetVertex<Data>> visited = new HashSet<NeighborHashSetVertex<Data>>();
			ArrayList<NeighborHashSetEdge<Data>> newEdges = new ArrayList<NeighborHashSetEdge<Data>>();
			for (NeighborHashSetVertex<Data> v: vertices){
				for (NeighborHashSetVertex<Data> n: v.neighbors){
					if (!visited.contains(n)){
						newEdges.add(new NeighborHashSetEdge<Data>(v,n));
					}
				}
				visited.add(v);
			}
			edges = newEdges;
			edgeChanged = false;
		}
		return edges;
	}
	
	
	public static interface Convertor< OldData, NewData > {
		NewData convert( NeighborHashSetVertex<? extends OldData> old );
		NewData convertix( Vertex<? extends OldData> old );
	}
	
	/**
	 * Does <i>NOT</i> make a deep copy of the vertices' data.
	 * 
	 * @author tw team
	 *
	 * @param <CopiedData>
	 */
	public static class Copier<CopiedData> implements Convertor<CopiedData,CopiedData> {
		public CopiedData convert(NeighborHashSetVertex<? extends CopiedData> old) {
			return old.data;
		}
		public CopiedData convertix(Vertex<? extends CopiedData> old) {
			return old.data;
		}	
	}
	
	public static <CopiedData> NeighborHashSetGraph<CopiedData> shallowCopy( NeighborHashSetGraph<CopiedData> g ){
		return copy(g,new Copier<CopiedData>());
	}
	
	public static < OldData, NewData > NeighborHashSetGraph<NewData> copy( NeighborHashSetGraph<OldData> oldG, Convertor<OldData,NewData> dataConvertor ) {

		// The new graph 
		NeighborHashSetGraph<NewData> newG = new NeighborHashSetGraph<NewData>();
		
		// Convert the vertices; build a translation table
		HashMap<NeighborHashSetVertex<OldData>,NeighborHashSetVertex<NewData>> oldToNewVertex = new HashMap<NeighborHashSetVertex<OldData>,NeighborHashSetVertex<NewData>>();
		for( NeighborHashSetVertex<OldData> oldVertex : oldG.vertices ) {
			// Create a new vertex from the old one
			NeighborHashSetVertex<NewData> newVertex = new NeighborHashSetVertex<NewData>();
			newVertex.data = dataConvertor.convert( oldVertex );
			oldToNewVertex.put( oldVertex, newVertex );
			newG.addVertex( newVertex );
		}
		
		// now translate all the edges.
		for( NeighborHashSetEdge<OldData> e : oldG.getEdges() ) {
			NeighborHashSetVertex<NewData> newA = oldToNewVertex.get(e.a);
			NeighborHashSetVertex<NewData> newB = oldToNewVertex.get(e.b);
			newG.addEdge( newA, newB );
		}
		
		// done!
		return newG;
		
	}
	
	
	public void contractEdge(NeighborHashSetVertex<Data> vertex1, NeighborHashSetVertex<Data> vertex2){
		
		//Select the vertex with the highest degree
		NeighborHashSetVertex<Data> v1,v2;
		
		if(vertex1.neighbors.size() < vertex2.neighbors.size()){
			v1 = vertex2;
			v2 = vertex1;
		} else {
			v1 = vertex1;
			v2 = vertex2;
		}
		
		//Remove the edge from the edgelists of the vertex
		v1.neighbors.remove(v2);
		v2.neighbors.remove(v1);
		
		//Add vertices of v1 to the list and remove the old edge from those vertices
		for(NeighborHashSetVertex<Data> n : v2.neighbors) {
			ensureEdge(v1,n);
			//ed.other(v2).edges.remove(ed);
		}
		
		//Remove the other vertex
		removeVertex(v2);
		//vertices.remove(v2);
		edgeChanged = true;
		
	}
	
	public void removeVertex( NeighborHashSetVertex<Data> v) {
		for(NeighborHashSetVertex<Data> n: v.neighbors){
			if(n==v)
				System.out.println("WTF>>>>edgo to myself");
			n.neighbors.remove(v);
		}
		
		vertices.remove(v);
		edgeChanged = true;
	}
	
	/**
	 * Eliminates a vertex from the copy of the graph by marrying the neighbors and removing the vertex.<br/>
	 * This method does <b>NOT</b> update the edgelist of the copy of the graph, because it is not used.
	 * 
	 * @param v The vertex to remove from the copy of the graph.
	 */
	public <T> void eliminateVertex(NeighborHashSetVertex<T> v){
		LinkedList<NeighborHashSetVertex<T>> neighbors = new LinkedList<NeighborHashSetVertex<T>>();
		for (NeighborHashSetVertex<T> other: v.neighbors){
			if (!other.neighbors.remove(v)){
				System.out.println("Borked, did not remove edge.");
			}
			for(NeighborHashSetVertex<T> n: neighbors){
				ensureEdge(other,n);
			}
			neighbors.add(other);
		}
		vertices.remove(v);
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
	private <T> void ensureEdge(NeighborHashSetVertex<T> v1, NeighborHashSetVertex<T> v2){
		if (!v1.neighbors.contains(v2)){
			v1.neighbors.add(v2);
			v2.neighbors.add(v1);
		}
		edgeChanged = true;
	}
	
		
	/**
	 * Makes sure the cached edgelist is no longer used. Call this function if you change something in the vertices of the graph without using the methods in Graph. 
	 */
	public void clearEdgeCache(){
		edgeChanged = true;
	}

	/**********************
	 * Warning - Testingfunction for QuickBB3 : Work in progress
	 **********************/
	
	public <T> ArrayList<NeighborHashSetEdge<T>> eliminateVertex2(NeighborHashSetVertex<T> v){
		ArrayList<NeighborHashSetEdge<T>> addedEdges = new ArrayList<NeighborHashSetEdge<T>>(); 
		LinkedList<NeighborHashSetVertex<T>> neighbors = new LinkedList<NeighborHashSetVertex<T>>();
		for (NeighborHashSetVertex<T> other: v.neighbors){
			if (!other.neighbors.remove(v)){
				System.out.println("Borked, did not remove edge.");
			}
			for(NeighborHashSetVertex<T> n: neighbors){
				NeighborHashSetEdge<T> e = ensureEdge2(other,n);
				if(e!=null)
					addedEdges.add(e);
			}
			neighbors.add(other);
		}
		vertices.remove(v);
		edgeChanged = true;
		return addedEdges;
	}
	
	private <T> NeighborHashSetEdge<T> ensureEdge2(NeighborHashSetVertex<T> v1, NeighborHashSetVertex<T> v2){
		if (!v1.neighbors.contains(v2)){
			v1.neighbors.add(v2);
			v2.neighbors.add(v1);
			return new NeighborHashSetEdge<T>(v1,v2);
		}
		edgeChanged = true;
		return null;
	}
	
	public void deEliminateVertex(NeighborHashSetVertex<Data> v, ArrayList<NeighborHashSetEdge<Data>> addedEdges) {
		//	Voeg vertex weer toe
		addVertex(v);
		for(NeighborHashSetVertex<Data> vx : v.neighbors) {
			vx.neighbors.add(v);			
		}
		
		//Verwijder toegevoegde edges
		for(NeighborHashSetEdge<Data> e : addedEdges) {
			removeEdge(e);
		}
		edgeChanged = true;
		
	}
	
	public void removeEdge(NeighborHashSetEdge<Data> e) {
		e.a.neighbors.remove(e.b);
		e.b.neighbors.remove(e.a);
	}
	
	public ArrayList<NeighborHashSetVertex<Data>> getSimplicialVertices() {
		ArrayList<NeighborHashSetVertex<Data>> simplicials = new ArrayList<NeighborHashSetVertex<Data>>();
		for( NeighborHashSetVertex<Data> v : vertices) {
			if(testSimplicial(v))
				simplicials.add(v);
		}
		return simplicials;
	}

	private boolean testSimplicial(NeighborHashSetVertex<Data> v) {
		for(NeighborHashSetVertex<Data> neighbor1: v.neighbors) {
			for(NeighborHashSetVertex<Data> neighbor2: v.neighbors) {
				if(neighbor1.data != neighbor2.data)
					if(!neighbor1.neighbors.contains(neighbor2))
						return false;				
			}
		}
		return true;
	}
	

}

