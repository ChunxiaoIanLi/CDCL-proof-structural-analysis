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
import java.util.Iterator;

public class ListGraph<D> extends NGraph< D > {

	/**
	 * <p>The vertex list for this graph is stored in an ArrayList</p>
	 * <p>TODO This would be nicer as a protected field, but right now
	 * it is convenient to have it public.</p>
	 */
	public ArrayList<NVertex<D>> vertices; 
	
	public ListGraph() {
		vertices = new ArrayList<NVertex<D>>();
	}

	@Override
	public NVertex<D> getVertex(int i) {
		return vertices.get(i);
	}

	@Override
	public Iterator<NVertex<D>> getVertices() {
		return vertices.iterator();
		//return new BorkIterator<NVertex<D>>( vertices );
	}
	
	public int getNumberOfVertices() {
		return vertices.size();
	}

	@Override
	public void addVertex(NVertex<D> v) {
		vertices.add( v );	
	}

	@Override
	public void removeVertex(NVertex<D> v) {
		vertices.remove( v );
		for(NVertex<D> ov : v)
			ov.removeNeighbor(v);
	}

	@Override
	public void setVertices(ArrayList<NVertex<D>> vs) {
		vertices = vs;
	}
	
	@Override
	public NGraph<D> copy() {
		
		NGraph<D> newG = new ListGraph<D>();
		
		HashMap<NVertex<D>, NVertex<D>> oldToNew = new HashMap<NVertex<D>, NVertex<D>>();
		
		for( NVertex<D> v : this ) {
			NVertex<D> nv = v.newOfSameType( v.data );
			newG.addVertex( nv );
			oldToNew.put( v, nv );
		}
		int size = getNumberOfVertices();
		for( int i=0; i<size; ++i ) {
			NVertex<D> v = vertices.get(i);
			for( NVertex<D> n : v ) {
				oldToNew.get(v).addNeighbor(oldToNew.get(n));
			}
		}
		
		return newG;
		
	}

}
