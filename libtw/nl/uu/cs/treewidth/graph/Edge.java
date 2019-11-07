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


/**
 * <p><emph>Deprecated! Use the NGraph instead.</emph></p>
 * An edge in the standard Graph datastructure.
 * 
 * @see Graph 
 * @author tw team
 * @param <Data> 
 *
 */
@Deprecated
public class Edge< Data > {
	
	/**
	 * An endpoint of the edge. The difference between a and b
	 * has no meaning.
	 * @see Edge#other  
	 */
	public Vertex<Data> a;
	/**
	 * An endpoint of the edge. The difference between a and b
	 * has no meaning.
	 * @see Edge#other  
	 */
	public Vertex<Data> b;
	
	/**
	 * An edge from v1 to v2.
	 * 
	 * @param v1
	 * @param v2
	 */
	public Edge( Vertex<Data> v1, Vertex<Data> v2 ) {
		a = v1;
		b = v2;
	}
	
	/**
	 * Useful for `getting to the other side' of an edge.<br />
	 * (TODO maybe give an example.) 
	 * @param from Should be one of the two endpoints of the edge.
	 * @return An endpoint of the edge which is not from.
	 */
	public Vertex<Data> other( Vertex<Data> from ) {
		return a==from? b : a;
	}
	
	public String toString() {
		return "edge("+a.data.toString()+","+b.data.toString()+")";
	}

}
