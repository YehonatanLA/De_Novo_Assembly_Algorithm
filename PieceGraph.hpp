#ifndef PIECEGRAPH_HPP_
#define PIECEGRAPH_HPP_

#include <vector>
#include <cassert>
#include <random>
#include <unordered_map>
#include <iso646.h>
using namespace std;

const int NA = -1;

struct SubpieceMatch {
	vector<int> suffixOf;
	vector<int> prefixOf;
};

struct Edge {
	int from;
	int to; // index of piece edge enters
	int subpieceLen; // length of connecting subpiece
	Edge() :
			from(), to(), subpieceLen() {
	}
	Edge(const int from, const int to, const int subpieceLen) :
			from(from), to(to), subpieceLen(subpieceLen) {
	}
	bool operator<(const Edge& a) const {
		if (this->from == a.from) {
			if (this->to == a.to) {
				return this->subpieceLen < a.subpieceLen;
			}
			else
				return this->to < a.to;
		}
		else
			return this->from < a.from;
	}

	bool operator==(const Edge& a) const {
		return !(*this < a) and !(a < *this);
	}
};

const Edge ZERO_EDGE = Edge(NA,NA,0);

// piece subpiece matches
struct PieceEdges {
	// matches of prefixes of piece with suffixes of other pieces.
	vector<Edge> in;
	// matches of suffixes of piece with prefixes of other pieces.
	vector<Edge> out;

	bool IsMultiEdgeOut(const Edge& outEdge) const {
		int countOutEdges = 0;
		for (auto& edge : out) {
			assert(edge.from == outEdge.from);
			if (edge.to == outEdge.to) {
				countOutEdges++;
				if (countOutEdges == 2) {
					return true;
				}
			}
		}
		assert(countOutEdges == 1);
		return false;
	}

	// repeated string case
	bool OverlapIsRepeatedString(const Edge& outEdge) const {
		int countOutEdges = 0;
		int minWeight = outEdge.subpieceLen / 2;
		for (auto& edge : out) {
			assert(edge.from == outEdge.from);
			if (edge.to == outEdge.to and edge.subpieceLen >= minWeight) {
				countOutEdges++;
				if (countOutEdges == 2) {
					return true;
				}
			}
		}
		assert(countOutEdges == 1);
		return false;
	}

	// assuming sorted in ascending order of from
	int MaxIn() const {
		if (in.empty())
			return NA;
		else
			return in.back().from;
	}
	int MaxOut() const {
		if (out.empty())
			return NA;
		else
			return out.back().to;
	}

	bool operator<(const PieceEdges& rhs) const {
		return this->in.size() * this->out.size() < rhs.in.size() * rhs.out.size();
	}

	bool OutEdgeExists(const Edge& edge) const {
		for (auto& outEdge : out) {
			if (edge == outEdge) {
				return true;
			}
		}
		return false;
	}

	void FindOutEdges(const int toVertex, vector<Edge>& foundEdges) const {
		foundEdges.clear();
		for (auto& outEdge : out) {
			if (outEdge.to == toVertex) {
				foundEdges.push_back(outEdge);
			}
		}
	}

	void DeleteInEdge(const int from, const int subpieceLen) {
		for (vector<Edge>::iterator it = in.begin(); it != in.end(); it++) {
			if (it->from == from and it->subpieceLen == subpieceLen) {
				in.erase(it);
				return;
			}
		}
		assert(0);
	}
	void DeleteOutEdge(const int to, const int subpieceLen) {
		for (vector<Edge>::iterator it = out.begin(); it != out.end(); it++) {
			if (it->to == to and it->subpieceLen == subpieceLen) {
				out.erase(it);
				return;
			}
		}
		assert(0);
	}
};

string MakeStrand(const int length, mt19937& generator);
void EdgesByPieceFinal(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
		const int TL, const int k);
void EdgesByPieceFinalK(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
		const int TL, const int k);
void EdgesByPieceFast(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
		const int TL, const int k);
//void EdgesByPieceFastCustomHash(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L,
//		const int TH, const int TL, const int k);
//void EdgesByPieceFastMyHash(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
//		const int TL, const int k);
void THEdgesByPiece(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
		const int k, vector<int>& noOutPieces, unordered_map<string, vector<int>>& lenKPrefixes,
		vector<Edge>& atLeastTHOutEdges);
void BelowTHEdgesByPiece(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
		const int TL, const int k, const vector<int>& noOutPieces,
		const unordered_map<string, vector<int>>& lenKPrefixes);
vector<string> PieceCover(const string& original, const int n, const int L, mt19937& generator);
vector<string> PieceCoverFirstLast(const string& original, const int n, const int L, mt19937& generator);
int ConnectorCount(const int n, const int L, mt19937& generator, vector<int>& connectorCount);
bool IsRepeated(const string& A, int& repeatedSize);

#endif /* PIECEGRAPH_HPP_ */
