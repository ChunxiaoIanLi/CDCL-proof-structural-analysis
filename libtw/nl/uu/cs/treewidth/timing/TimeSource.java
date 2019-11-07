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
 
/**
 * 
 */
package nl.uu.cs.treewidth.timing;

/**
 * Interface used by {@link Stopwatch} as the source of `time.'<br />
 * For Stopwatch to make sense, the result of subsequent calls to now()
 * have to be non-decreasing (which is reasonable for `time').
 * 
 * @author tw team
 *
 */
public interface TimeSource {
	
	/**
	 * For Stopwatch to make sense, the result of subsequent calls to now()
	 * have to be non-decreasing (which is reasonable for `time').
	 * @return Some measure of `time.'
	 */
	public abstract long now();
}