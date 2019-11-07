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

import java.util.HashSet;
import java.util.Iterator;

public class HashVertex< D > extends NVertex< D > {

	HashSet<NVertex<D>> neighbors;
	
	public <T> HashVertex<T> newOfSameType( T d ) {
		return new HashVertex<T>( d );
	}
	
	public HashVertex() { init(); }
	public HashVertex( D d ) { super(d); init(); }
	private void init() {
		neighbors = new HashSet<NVertex<D>>();
	}

	@Override
	public boolean isNeighbor(NVertex<D> v) {
		return neighbors.contains( v );
	}
	@Override
	public boolean ensureNeighbor(NVertex<D> v) {
		return neighbors.add( v );
	}
	@Override
	public void addNeighbor(NVertex<D> v) {
		neighbors.add( v );
	}
	
	@Override
	public void removeNeighbor(NVertex<D> v) {
		neighbors.remove(v);
	}

	@Override
	public Iterator<NVertex<D>> getNeighbors() {
		return neighbors.iterator();
	}
	
	public HashVertex<D> copy() {
		return new HashVertex<D>(data);
	}
	@Override
	public int getNumberOfNeighbors() {
		return neighbors.size();
	}
	
}
