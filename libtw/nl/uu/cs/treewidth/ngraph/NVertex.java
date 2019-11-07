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

import java.util.Iterator;

public abstract class NVertex< D > implements Iterable<NVertex<D>> {

	public D data;
	
	public NVertex() {}
	public NVertex( D d ) {
		data = d;
	}
	
	// ====== To be implemented by implementing classes
	
	public abstract <T> NVertex<T> newOfSameType( T d );
	
	public abstract boolean isNeighbor( NVertex<D> v );
	public abstract boolean ensureNeighbor( NVertex<D> v );
	public abstract void addNeighbor( NVertex<D> v ); // precond: v is not a neighbor of this.
	
	
	public abstract void removeNeighbor( NVertex<D> v );
	
	public abstract Iterator<NVertex<D>> getNeighbors();
	public abstract int getNumberOfNeighbors();
	
	public Iterator<NVertex<D>> iterator() {
		return getNeighbors();
	}
	
	public abstract NVertex<D> copy();
	
}
