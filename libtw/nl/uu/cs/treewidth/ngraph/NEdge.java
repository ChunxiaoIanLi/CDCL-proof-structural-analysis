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

public class NEdge<D> {

	public NEdge( NVertex<D> a, NVertex<D> b ) {
		this.a = a;
		this.b = b;
	}
	public NVertex<D> a;
	public NVertex<D> b;
	
	public int hashCode() {
		return a.hashCode() ^ b.hashCode();
	}
	public boolean equals( Object o ) {
		if( o instanceof NEdge ) {
			NEdge e = (NEdge)o;
			return (a==e.a&&b==e.b) || (a==e.b&&b==e.a);
		} else return false;
	}
	
}
