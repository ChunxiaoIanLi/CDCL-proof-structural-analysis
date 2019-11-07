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

import java.util.HashMap;

import nl.uu.cs.treewidth.graph.Edge;
import nl.uu.cs.treewidth.graph.Graph;
import nl.uu.cs.treewidth.graph.Vertex;

public class Utility {
	
	public static <D> NGraph<D> newify( Graph<D> g ) {
		
		NGraph<D> newG = new ListGraph<D>();
		
		HashMap<Vertex<D>, NVertex<D>> oldToNew = new HashMap<Vertex<D>, NVertex<D>>();
		
		for( Vertex<D> v : g.vertices ) {
			NVertex<D> nv = new ListVertex<D>( v.data );
			newG.addVertex( nv );
			oldToNew.put( v, nv );
		}
		for( Edge<D> e : g.getEdges() ) {
			newG.ensureEdge( oldToNew.get(e.a), oldToNew.get(e.b) );
		}
		
		return newG;
		
	}
	
	
	
}
