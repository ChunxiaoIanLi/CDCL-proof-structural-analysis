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

@Deprecated
public class VertexOrder {
	
	public ArrayList<Vertex<? extends InputData>> vertices;
	
	public VertexOrder() {
		vertices = new ArrayList<Vertex<? extends InputData>>();
	}
	
	public VertexOrder( VertexOrder other ) {
		vertices = new ArrayList<Vertex<? extends InputData>>(  other.vertices );
	}	 
	
	public static interface NamedData {
		public abstract String getName();
	}
	
	public String toString() {
		String s = "";
		for( Vertex<? extends InputData> v : vertices) {
			s = s.concat( " " + v.data.toString() );
		}
		return s;
	}
	
}