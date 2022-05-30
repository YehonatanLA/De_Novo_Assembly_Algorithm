#include <string>
#include <random>
#include <set>
#include <unordered_set>
#include <algorithm>
#include <unordered_map>
#include <iostream>
#include "PieceGraph.hpp"
#include "Utils.hpp"
using namespace std;

string MakeStrand(const int length, mt19937& generator) {
	string strand;
	uniform_int_distribution<int> distribution(0, 3);
	string letters("GTAC");
	for (int i = 0; i < length; i++) {
		strand += letters[distribution(generator)];
	}
	return strand;
}

//bool IsCover(const set<int>& positions, const int n, const int L) {
//
//	if (*positions.begin() != 0)
//		return false;
//	int lastPosition = *positions.rbegin();
//	if (lastPosition != n - L)
//		return false;
//	int prevPosition = 0;
//	for (auto& position : positions) {
//		if (position - prevPosition >= L)
//			return false;
//		prevPosition = position;
//	}
//	return true;
//}

bool IsCover2(const set<int>& positions, const int n, const int L, const int lastGood, int& nextLastGood) {
	assert(*positions.begin() == 0);
	int lastPosition = *positions.rbegin();
	assert(lastPosition == n - L);

	set<int>::const_iterator posIt = positions.begin();
	if (lastGood > 0) {
		posIt = positions.find(lastGood);
	}
	int prevPosition = lastGood;
	for (; posIt != positions.end(); posIt++) {
		int position = *posIt;
		if (position - prevPosition >= L) {
			nextLastGood = prevPosition;
			return false;
		}
		prevPosition = position;
	}
	return true;
}

// return a vector of unique *position* random L-length pieces of the n-length original which cover the original
// assuming L multiple of n
// the substrings cover the original - each letter of the original is in at least one of the substrings

vector<string> PieceCover(const string& original, const int n, const int L, mt19937& generator) {
	vector<string> cover;
	vector<int> substringStart;
	set<int> positions;
	for (int i = 0; i <= n - L; i++) {
		substringStart.push_back(i);
	}

	shuffle(substringStart.begin(), substringStart.end(), generator);
	int substringStartIndex = 0;
	int newPosition;
	bool zeroPosition = false, nMinusLPosition = false;
	// add to cover until 0 piece and n-L piece are chosen
	while ((not zeroPosition) or (not nMinusLPosition)) {
		newPosition = substringStart[substringStartIndex++];
		if (newPosition == 0)
			zeroPosition = true;
		else if (newPosition == n - L)
			nMinusLPosition = true;
		positions.insert(newPosition);
	}

	int lastGood = 0, nextLastGood = 0;
	while (not IsCover2(positions, n, L, lastGood, nextLastGood)) {
		lastGood = nextLastGood;
		do {
			newPosition = substringStart[substringStartIndex++];
			positions.insert(newPosition);
		} while (newPosition < lastGood or newPosition - lastGood >= L);
	}

	for (auto& position : positions) {
		cover.push_back(original.substr(position, L));
	}

	shuffle(cover.begin(), cover.end(), generator);
	return cover;
}

vector<string> PieceCoverFirstLast(const string& original, const int n, const int L, mt19937& generator) {
	vector<string> cover;
	vector<int> substringStart;
	set<int> positions = { 0, n - L };
	for (int i = 1; i < n - L; i++) {
		substringStart.push_back(i);
	}
	int minSubstringNum = n / L;
	shuffle(substringStart.begin(), substringStart.end(), generator);
	for (int i = 0; i < minSubstringNum; i++) {
		positions.insert(substringStart[i]);
	}

	int substringStartIndex = minSubstringNum;
	int lastGood = 0, nextLastGood = 0;
	int newPosition;
	while (not IsCover2(positions, n, L, lastGood, nextLastGood)) {
		lastGood = nextLastGood;
		do {
			newPosition = substringStart[substringStartIndex++];
			positions.insert(newPosition);
		} while (newPosition < lastGood or newPosition - lastGood >= L);
	}

	for (auto& position : positions) {
		cover.push_back(original.substr(position, L));
	}

	shuffle(cover.begin(), cover.end(), generator);
	return cover;
}

int ConnectorCount(const int n, const int L, mt19937& generator, vector<int>& connectorCount) {
	connectorCount = vector<int>(L);
	vector<string> cover;
	vector<int> substringStart;
	set<int> positions;
	for (int i = 0; i <= n - L; i++) {
		substringStart.push_back(i);
	}

	shuffle(substringStart.begin(), substringStart.end(), generator);
	int substringStartIndex = 0;
	int newPosition;
	bool zeroPosition = false, nMinusLPosition = false;
	// add to cover until 0 piece and n-L piece are chosen
	while ((not zeroPosition) or (not nMinusLPosition)) {
		newPosition = substringStart[substringStartIndex++];
		if (newPosition == 0)
			zeroPosition = true;
		else if (newPosition == n - L)
			nMinusLPosition = true;
		positions.insert(newPosition);
	}

	int lastGood = 0, nextLastGood = 0;
	while (not IsCover2(positions, n, L, lastGood, nextLastGood)) {
		lastGood = nextLastGood;
		do {
			newPosition = substringStart[substringStartIndex++];
			positions.insert(newPosition);
		} while (newPosition < lastGood or newPosition - lastGood >= L);
	}

	vector<int> positionsVec(positions.begin(), positions.end());
	sort(positionsVec.begin(), positionsVec.end());
	for (unsigned i = 1; i < positionsVec.size(); i++) {
		int currentConnectorLen = L - (positionsVec[i] - positionsVec[i - 1]);
		connectorCount[currentConnectorLen]++;
	}
	return positionsVec.size();
}

//vector<string> UniquePieceCover(string& original, const int n, const int L, mt19937& generator) {
//	vector<string> cover;
//	set<string> uniquePieces;
//	do {
//		original = MakeStrand(n, generator);
//		cover.clear();
//		uniquePieces.clear();
//		vector<int> substringStart;
//		set<int> positions;
//		for (int i = 0; i < n - L + 1; i++) {
//			substringStart.push_back(i);
//		}
//		int minSubstringNum = n / L;
//		shuffle(substringStart.begin(), substringStart.end(), generator);
//		for (int i = 0; i < minSubstringNum; i++) {
//			positions.insert(substringStart[i]);
//		}
//
//		int substringStartIndex = minSubstringNum;
//		while (not IsCover(positions, n, L)) {
//			positions.insert(substringStart[substringStartIndex++]);
//		}
//
//		for (auto& position : positions) {
//			cover.push_back(original.substr(position, L));
//		}
//		uniquePieces.insert(cover.begin(), cover.end());
//	} while (cover.size() != uniquePieces.size());
//	shuffle(cover.begin(), cover.end(), generator);
//	return cover;
//}

void SubpieceHashTable(const vector<string>& cover, unordered_map<string, SubpieceMatch>& subpieceHashTable,
		const int L) {
	string prefix, suffix;
	subpieceHashTable.clear();
	for (unsigned substringIndex = 0; substringIndex < cover.size(); substringIndex++) {
		for (int len = 1; len < L; len++) {
			prefix = cover[substringIndex].substr(0, len);
			subpieceHashTable[prefix].prefixOf.push_back(substringIndex);
			suffix = cover[substringIndex].substr(L - len);
			subpieceHashTable[suffix].suffixOf.push_back(substringIndex);
		}
	}
}

void SubpieceHashTableMax(const vector<string>& cover, unordered_map<string, SubpieceMatch>& subpieceHashTable,
		const int L, const int maxSubpieceLen) {
	string prefix, suffix;
	subpieceHashTable.clear();
	for (unsigned substringIndex = 0; substringIndex < cover.size(); substringIndex++) {
		for (int len = 1; len <= maxSubpieceLen; len++) {
			prefix = cover[substringIndex].substr(0, len);
			subpieceHashTable[prefix].prefixOf.push_back(substringIndex);
			suffix = cover[substringIndex].substr(L - len);
			subpieceHashTable[suffix].suffixOf.push_back(substringIndex);
		}
	}
}

void SubpieceHashTableMax(const vector<string>& cover, const vector<int>& noOutPieces, const vector<int>& noInPieces,
		unordered_map<string, SubpieceMatch>& subpieceHashTable, const int L, const int maxSubpieceLen) {
	string prefix, suffix;
	subpieceHashTable.clear();
	for (auto& substringIndex : noOutPieces) {
		for (int len = 1; len <= maxSubpieceLen; len++) {
			suffix = cover[substringIndex].substr(L - len);
			subpieceHashTable[suffix].suffixOf.push_back(substringIndex);
		}
	}
	for (auto& substringIndex : noInPieces) {
		for (int len = 1; len <= maxSubpieceLen; len++) {
			prefix = cover[substringIndex].substr(0, len);
			subpieceHashTable[prefix].prefixOf.push_back(substringIndex);
		}
	}
}

struct CompEdgeByLenAsc {
	bool operator()(const Edge& a, const Edge& b) const {
		return a.subpieceLen < b.subpieceLen;
	}
};

// for each string of the cover by index:
// matches of prefixes with suffixes of other strings (matched string index, suffix len)
// matches of suffixes with prefixes of other strings (matched string index, prefix len)
// edges sorted in ascending order of subpieceLen

//void EdgesByPiece(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L) {
//	unordered_map<string, SubpieceMatch> subpieceHashTable;
//	SubpieceHashTable(cover, subpieceHashTable, L);
//	edgesByPiece = vector<PieceEdges>(cover.size());
//	for (auto& pr : subpieceHashTable) {
//		string subpiece = pr.first;
//		const SubpieceMatch& subInfo = pr.second;
//		const vector<int>& prefixOf = subInfo.prefixOf;
//		const vector<int>& suffixOf = subInfo.suffixOf;
//		if (prefixOf.empty() or suffixOf.empty())
//			continue;
//		for (auto& prIndex : prefixOf) {
//			for (auto& sfIndex : suffixOf) {
//				if (prIndex == sfIndex)
//					continue; // to avoid self edges
//				Edge edge(sfIndex, prIndex, subpiece.size());
//				edgesByPiece[prIndex].in.push_back(edge);
//				edgesByPiece[sfIndex].out.push_back(edge);
//			}
//		}
//	}
//	CompEdgeByLenAsc compEdgeByLenAsc;
//	for (auto& piece : edgesByPiece) {
//		sort(piece.in.begin(), piece.in.end(), compEdgeByLenAsc);
//		sort(piece.out.begin(), piece.out.end(), compEdgeByLenAsc);
//	}
//}

bool SuffixAIsPrefixB(const string& A, const string& B, const int L, const int len) {
	for (int i = 0; i < len; i++) {
		if (A[L - len + i] != B[i])
			return false;
	}
	return true;
}

void EdgesByPieceMax(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L,
		const int maxSubpieceLen) {
	unordered_map<string, SubpieceMatch> subpieceHashTable;
	SubpieceHashTableMax(cover, subpieceHashTable, L, maxSubpieceLen);
	for (auto& pr : subpieceHashTable) {
		string subpiece = pr.first;
		const SubpieceMatch& subInfo = pr.second;
		const vector<int>& prefixOf = subInfo.prefixOf;
		const vector<int>& suffixOf = subInfo.suffixOf;
		if (prefixOf.empty() or suffixOf.empty())
			continue;
		for (auto& prIndex : prefixOf) {
			for (auto& sfIndex : suffixOf) {
				if (prIndex == sfIndex)
					continue; // to avoid self edges
				Edge edge(sfIndex, prIndex, subpiece.size());
				edgesByPiece[prIndex].in.push_back(edge);
				edgesByPiece[sfIndex].out.push_back(edge);
			}
		}
	}
}

void EdgesByPieceMax(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const vector<int>& noOutPieces,
		const vector<int>& noInPieces, const int L, const int maxSubpieceLen) {
	unordered_map<string, SubpieceMatch> subpieceHashTable;
	SubpieceHashTableMax(cover, noOutPieces, noInPieces, subpieceHashTable, L, maxSubpieceLen);
	for (auto& pr : subpieceHashTable) {
		string subpiece = pr.first;
		const SubpieceMatch& subInfo = pr.second;
		const vector<int>& prefixOf = subInfo.prefixOf;
		const vector<int>& suffixOf = subInfo.suffixOf;
		if (prefixOf.empty() or suffixOf.empty())
			continue;
		for (auto& prIndex : prefixOf) {
			for (auto& sfIndex : suffixOf) {
				if (prIndex == sfIndex)
					continue; // to avoid self edges
				Edge edge(sfIndex, prIndex, subpiece.size());
				edgesByPiece[prIndex].in.push_back(edge);
				edgesByPiece[sfIndex].out.push_back(edge);
			}
		}
	}
}

vector<int> AllSuffixAIsPrefixB(const string& A, const string& B, const int L,
		const unordered_map<string, vector<int> >& lenkInstances, const int k) {
	vector<int> lens;
//	for (int len = 1; len < k; len++) {
//		if (SuffixAIsPrefixB(A, B, L, len))
//			lens.push_back(len);
//	}
	string kLenPrefixB = B.substr(0, k);
	auto foundPrefixB = lenkInstances.find(kLenPrefixB);
	if (foundPrefixB == lenkInstances.end())
		return lens;
	const vector<int>& prefixBInstances = foundPrefixB->second;
	for (auto& position : prefixBInstances) {
		int len = L - position;
		if (SuffixAIsPrefixB(A, B, L, len))
			lens.push_back(len);
	}
	return lens;
}

// all len k substrings of str and their positions in str (except first k-substring at position 0)
void LenKInstances(const string& str, const int L, const int k, unordered_map<string, vector<int> >& lenkInstances) {
	for (int i = 1; i < L - k + 1; i++) {
		lenkInstances[str.substr(i, k)].push_back(i);
	}
}

//void EdgesByPieceFast(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int k) {
//	int coverSize = cover.size();
//	edgesByPiece = vector<PieceEdges>(coverSize);
//	EdgesByPieceMax(edgesByPiece, cover, L, k - 1); // takes care of edge up to k-1
//	for (int i = 0; i < coverSize; i++) {
//		unordered_map<string, vector<int> > lenkInstances;
//		LenKInstances(cover[i], L, k, lenkInstances);
//		for (int j = 0; j < coverSize; j++) {
//			if (i == j)
//				continue;
//			vector<int> suffixAPrefixB = AllSuffixAIsPrefixB(cover[i], cover[j], L, lenkInstances, k);
//			for (auto& len : suffixAPrefixB) {
//				Edge edge(i, j, len);
//				edgesByPiece[i].out.push_back(edge);
//				edgesByPiece[j].in.push_back(edge);
//			}
//		}
//	}
//	CompEdgeByLenAsc compEdgeByLenAsc;
//	for (auto& piece : edgesByPiece) {
//		sort(piece.in.begin(), piece.in.end(), compEdgeByLenAsc);
//		sort(piece.out.begin(), piece.out.end(), compEdgeByLenAsc);
//	}
//}

// for a given k len string - conPref
struct EdgePrefixCandidates {
	unordered_map<int, vector<int> > out; // (piece, positions of conPref in piece)
	vector<int> in; // strings with prefix conPref
};

bool SuffixAIsPrefixB(const string& A, const string& B, const int L, const int len, const int k) {
	for (int i = k; i < len; i++) {
		if (A[L - len + i] != B[i])
			return false;
	}
	return true;
}

void ConnectorPrefixCandidates(const vector<string>& cover, unordered_map<string, EdgePrefixCandidates>& prefixCand,
		const int k, const int L) {
	int coverSize = cover.size();
	// pieces by their k len prefix
	for (int piece = 0; piece < coverSize; piece++) {
		prefixCand[cover[piece].substr(0, k)].in.push_back(piece);
	}
	// if k len substring of piece matches a k len prefix of another string, add it as candidate
	for (int piece = 0; piece < coverSize; piece++) {
		for (int i = 1; i < L - k + 1; i++) {
			string substring = cover[piece].substr(i, k);
			auto found = prefixCand.find(substring);
			if (found == prefixCand.end())
				continue;
			found->second.out[piece].push_back(i);
		}
	}
}

//void EdgesByPieceFast2(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int k) {
//	int coverSize = cover.size();
//	edgesByPiece = vector<PieceEdges>(coverSize);
//	EdgesByPieceMax(edgesByPiece, cover, L, k - 1); // takes care of edge up to k-1
//	unordered_map<string, EdgePrefixCandidates> prefixCand;
//	ConnectorPrefixCandidates(cover, prefixCand, k, L);
//	for (auto& pr : prefixCand) {
//		for (auto& BIndex : pr.second.in) {
//			for (auto& outPr : pr.second.out) {
//				int AIndex = outPr.first;
//				for (auto& position : outPr.second) {
//					int len = L - position;
//					if (SuffixAIsPrefixB2(cover[AIndex], cover[BIndex], L, len, k)) {
//						Edge edge(AIndex, BIndex, len);
//						edgesByPiece[AIndex].out.push_back(edge);
//						edgesByPiece[BIndex].in.push_back(edge);
//					}
//				}
//			}
//		}
//	}
//
//	CompEdgeByLenAsc compEdgeByLenAsc;
//	for (auto& piece : edgesByPiece) {
//		sort(piece.in.begin(), piece.in.end(), compEdgeByLenAsc);
//		sort(piece.out.begin(), piece.out.end(), compEdgeByLenAsc);
//	}
//}

void LenKPrefixes(const vector<string>& cover, unordered_map<string, vector<int> >& lenKPrefixes, const int k) {
	int coverSize = cover.size();
	for (int piece = 0; piece < coverSize; piece++) {
		lenKPrefixes[cover[piece].substr(0, k)].push_back(piece);
	}
}

//void LenKPrefixesMyHash(const vector<string>& cover, HashMap<vector<int> >& lenKPrefixes, const int k) {
//	int coverSize = cover.size();
//	for (int piece = 0; piece < coverSize; piece++) {
//		lenKPrefixes[cover[piece].substr(0, k)].push_back(piece);
//	}
//}

// check if A is a repeated string. if it is, set repeatedStr to repeated string
bool IsRepeated(const string& A, int& repeatedSize) {
	assert(A.size() >= 2);
	string AA = A + A;
	auto position = AA.find(A, 1);
	if (position != A.size()) {
		repeatedSize = position;
		return true;
	}
	else {
		return false;
	}
}

int LongestPrefixSuffix(const string& s) {
	int n = s.length();

	int lps[n];
	lps[0] = 0; // lps[0] is always 0

	// length of the previous longest prefix suffix
	int len = 0;

	// the loop calculates lps[i] for i = 1 to n-1
	int i = 1;
	while (i < n) {
		if (s[i] == s[len]) {
			len++;
			lps[i] = len;
			i++;
		}
		else // (pat[i] != pat[len])
		{
			// This is tricky. Consider the example. AAACAAAA and i = 7. The idea is similar to search step.
			if (len != 0) {
				len = lps[len - 1];

				// Also, note that we do not increment i here
			}
			else // if (len == 0)
			{
				lps[i] = 0;
				i++;
			}
		}
	}

	int res = lps[n - 1];

	// Since we are looking for
	// non overlapping parts.
	return (res > n / 2) ? res / 2 : res;
}

// the string can be represented as M-...M-Prefix of M
// return length of M
int AlmostRepeated(const string& str) {
	int strLen = str.length();
	int longestPrefixSuffix = LongestPrefixSuffix(str);
	if (longestPrefixSuffix == 0)
		return strLen;
	int mLen;
	string strTmp = str.substr(0, strLen - longestPrefixSuffix);
	if (IsRepeated(strTmp, mLen)) {
		return mLen;
	}
	else
		return strLen - longestPrefixSuffix;
}

bool PrefixIsAlmostRepeated(const string& str, const int prefixLen, int& mLen) {
	mLen = AlmostRepeated(str.substr(0, prefixLen));
	return prefixLen != mLen;
}

void THEdgesByPiece(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
		const int k, vector<int>& noOutPieces, unordered_map<string, vector<int>>& lenKPrefixes,
		vector<Edge>& atLeastTHOutEdges) {
	assert(TH < L and k < TH and k > 3);
	int coverSize = cover.size();

	int kLenPrefixMaxNum = round(pow(4, k));
	int hashTSize = min(kLenPrefixMaxNum, coverSize);
	lenKPrefixes = unordered_map<string, vector<int>>(hashTSize); // (len k prefix, vector of pieces)
	LenKPrefixes(cover, lenKPrefixes, k);
	noOutPieces = vector<int>(cover.size());
	// put all pieces in noOutPieces
	for (int piece = 0; piece < coverSize; piece++)
		noOutPieces[piece] = piece;

	// all longest matches with overlap >=TH
	for (int position = 1; position <= L - TH; position++) {
		for (vector<int>::iterator noOutIt = noOutPieces.begin(); noOutIt != noOutPieces.end();) {
			auto foundKMatch = lenKPrefixes.find(cover[*noOutIt].substr(position, k)); //find k len substring at position of current piece without out edge
			if (foundKMatch != lenKPrefixes.end()) { // no piece has prefix
				int len = L - position;
				bool itNotIncremented = true;
				for (auto prefixPieceIt = foundKMatch->second.begin(); prefixPieceIt != foundKMatch->second.end();) {
					if (SuffixAIsPrefixB(cover[*noOutIt], cover[*prefixPieceIt], L, len, k)) {
						Edge edge(*noOutIt, *prefixPieceIt, len);
						edgesByPiece[*noOutIt].out.push_back(edge);
						edgesByPiece[*prefixPieceIt].in.push_back(edge);
						atLeastTHOutEdges.push_back(edge);
						noOutIt = noOutPieces.erase(noOutIt);
						itNotIncremented = false;
						// erase matched prefix because it will not have any other real match
						prefixPieceIt = foundKMatch->second.erase(prefixPieceIt);
						if (foundKMatch->second.empty()) {
							lenKPrefixes.erase(foundKMatch);
						}
						break;
					}
					else {
						prefixPieceIt++;
					}
				}
				if (itNotIncremented)
					noOutIt++;
			}
			else {
				noOutIt++;
			}
		}
	}
}

//void THEdgesByPieceMyHashV2(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
//		const int k, vector<int>& noOutPieces, HashMap<vector<int> >& lenKPrefixes, vector<Edge>& atLeastTHOutEdges) {
//	assert(TH < L and k < TH and k > 3);
//	int coverSize = cover.size();
//
//	int kLenPrefixMaxNum = round(pow(4, k));
//	int hashTSize = min(kLenPrefixMaxNum, coverSize);
//	lenKPrefixes = HashMap<vector<int> >(hashTSize, k); // (len k prefix, vector of pieces)
//	LenKPrefixesMyHash(cover, lenKPrefixes, k);
//	noOutPieces = vector<int>(cover.size());
//	// put all pieces in noOutPieces
//	for (int piece = 0; piece < coverSize; piece++)
//		noOutPieces[piece] = piece;
//
//	// all longest matches with overlap >=TH
//	for (vector<int>::iterator noOutIt = noOutPieces.begin(); noOutIt != noOutPieces.end();) {
//		bool itIncremented = false;
//		int startPos = 1, endPos = L - TH;
//		int foundKeyPosition;
//		int bucketIndex, prevInBucketIndex, entryIndex;
//		unsigned lastHash;
//		while (1) {
//			vector<int> prefixVector;
//			bool foundKMatch = lenKPrefixes.GetFirstKeyMatch(cover[*noOutIt], startPos, endPos, prefixVector,
//					foundKeyPosition, lastHash, bucketIndex, prevInBucketIndex, entryIndex);
//			if (foundKMatch) { // no piece has prefix
//				int len = L - foundKeyPosition;
//				for (auto prefixPieceIt = prefixVector.begin(); prefixPieceIt != prefixVector.end();) {
//					if (SuffixAIsPrefixB(cover[*noOutIt], cover[*prefixPieceIt], L, len, k)) {
//						Edge edge(*noOutIt, *prefixPieceIt, len);
//						edgesByPiece[*noOutIt].out.push_back(edge);
//						edgesByPiece[*prefixPieceIt].in.push_back(edge);
//						atLeastTHOutEdges.push_back(edge);
//						noOutIt = noOutPieces.erase(noOutIt);
//						itIncremented = true;
//						// erase matched prefix because it will not have any other real match
//						prefixPieceIt = prefixVector.erase(prefixPieceIt);
//						if (prefixVector.empty()) {
//							lenKPrefixes.Delete(bucketIndex, prevInBucketIndex, entryIndex);
//						}
//						break;
//					}
//					else {
//						prefixPieceIt++;
//					}
//				}
//				startPos = foundKeyPosition + 1;
//			}
//			if (itIncremented or (not foundKMatch))
//				break;
//
//		}
//
//		if (not itIncremented)
//			noOutIt++;
//	}
//
//}

//void THEdgesByPieceMyHash(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
//		const int k, vector<int>& noOutPieces, HashMap<vector<int> >& lenKPrefixes, vector<Edge>& atLeastTHOutEdges) {
//	assert(TH < L and k < TH and k > 3);
//	int coverSize = cover.size();
//
//	int kLenPrefixMaxNum = round(pow(4, k));
//	int hashTSize = min(kLenPrefixMaxNum, coverSize);
//	lenKPrefixes = HashMap<vector<int> >(hashTSize, k); // (len k prefix, vector of pieces)
//	LenKPrefixesMyHash(cover, lenKPrefixes, k);
//	noOutPieces = vector<int>(cover.size());
//	// put all pieces in noOutPieces
//	for (int piece = 0; piece < coverSize; piece++)
//		noOutPieces[piece] = piece;
//
//	// all longest matches with overlap >=TH
//	for (vector<int>::iterator noOutIt = noOutPieces.begin(); noOutIt != noOutPieces.end();) {
//		bool itIncremented = false;
//		for (int position = 1; position <= L - TH; position++) {
//			vector<int> prefixVector;
//			int bucketIndex, prevInBucketIndex, entryIndex;
//			bool foundKMatch = lenKPrefixes.Get(cover[*noOutIt].substr(position, k), prefixVector, bucketIndex,
//					prevInBucketIndex, entryIndex); //find k len substring at position of current piece without out edge
//			if (foundKMatch) { // no piece has prefix
//				int len = L - position;
//				for (auto prefixPieceIt = prefixVector.begin(); prefixPieceIt != prefixVector.end();) {
//					if (SuffixAIsPrefixB(cover[*noOutIt], cover[*prefixPieceIt], L, len, k)) {
//						Edge edge(*noOutIt, *prefixPieceIt, len);
//						edgesByPiece[*noOutIt].out.push_back(edge);
//						edgesByPiece[*prefixPieceIt].in.push_back(edge);
//						atLeastTHOutEdges.push_back(edge);
//						noOutIt = noOutPieces.erase(noOutIt);
//						itIncremented = true;
//						// erase matched prefix because it will not have any other real match
//						prefixPieceIt = prefixVector.erase(prefixPieceIt);
//						if (prefixVector.empty()) {
//							lenKPrefixes.Delete(bucketIndex, prevInBucketIndex, entryIndex);
//						}
//						break;
//					}
//					else {
//						prefixPieceIt++;
//					}
//				}
//			}
//			if (itIncremented)
//				break;
//		}
//
//		if (not itIncremented)
//			noOutIt++;
//	}
//
//}

//struct GTACHasher {
//	size_t operator()(const string& str) const {
//		assert(str.size() <= 16);
//		size_t hash = 0;
//		for (auto& letter : str) {
//			hash <<= 2;
//			switch (letter) {
//			case 'A':
//				hash += 0;
//				break;
//			case 'C':
//				hash += 1;
//				break;
//			case 'G':
//				hash += 2;
//				break;
//			case 'T':
//				hash += 3;
//				break;
//			}
//		}
//		return hash;
//	}
//};

//void LenKPrefixes(const vector<string>& cover, unordered_map<string, vector<int>, GTACHasher>& lenKPrefixes,
//		const int k) {
//	int coverSize = cover.size();
//	for (int piece = 0; piece < coverSize; piece++) {
//		lenKPrefixes[cover[piece].substr(0, k)].push_back(piece);
//	}
//}
//
//void THEdgesByPieceCustomHash(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
//		const int k, vector<int>& noOutPieces, unordered_map<string, vector<int>, GTACHasher>& lenKPrefixes,
//		vector<Edge>& atLeastTHOutEdges) {
//	assert(TH < L and k < TH and k > 3);
//	int coverSize = cover.size();
//
//	int kLenPrefixMaxNum = round(pow(4, k));
//	int hashTSize = min(kLenPrefixMaxNum, coverSize);
//	lenKPrefixes = unordered_map<string, vector<int>, GTACHasher>(hashTSize); // (len k prefix, vector of pieces)
//	LenKPrefixes(cover, lenKPrefixes, k);
//	noOutPieces = vector<int>(cover.size());
//	// put all pieces in noOutPieces
//	for (int piece = 0; piece < coverSize; piece++)
//		noOutPieces[piece] = piece;
//
//	// all longest matches with overlap >=TH
//	for (int position = 1; position <= L - TH; position++) {
//		for (vector<int>::iterator noOutIt = noOutPieces.begin(); noOutIt != noOutPieces.end();) {
//			auto foundKMatch = lenKPrefixes.find(cover[*noOutIt].substr(position, k)); //find k len substring at position of current piece without out edge
//			if (foundKMatch != lenKPrefixes.end()) { // no piece has prefix
//				int len = L - position;
//				bool itNotIncremented = true;
//				for (auto prefixPieceIt = foundKMatch->second.begin(); prefixPieceIt != foundKMatch->second.end();) {
//					if (SuffixAIsPrefixB(cover[*noOutIt], cover[*prefixPieceIt], L, len, k)) {
//						Edge edge(*noOutIt, *prefixPieceIt, len);
//						edgesByPiece[*noOutIt].out.push_back(edge);
//						edgesByPiece[*prefixPieceIt].in.push_back(edge);
//						atLeastTHOutEdges.push_back(edge);
//						noOutIt = noOutPieces.erase(noOutIt);
//						itNotIncremented = false;
//						// erase matched prefix because it will not have any other real match
//						prefixPieceIt = foundKMatch->second.erase(prefixPieceIt);
//						if (foundKMatch->second.empty()) {
//							lenKPrefixes.erase(foundKMatch);
//						}
//						break;
//					}
//					else {
//						prefixPieceIt++;
//					}
//				}
//				if (itNotIncremented)
//					noOutIt++;
//			}
//			else {
//				noOutIt++;
//			}
//		}
//	}
//}

void BelowTHEdgesByPiece(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
		const int TL, const int k, const vector<int>& noOutPieces,
		const unordered_map<string, vector<int>>& lenKPrefixes) {

	vector<int> noInPieces;
	for (auto& pr : lenKPrefixes) {
		noInPieces.insert(noInPieces.end(), pr.second.begin(), pr.second.end());
	}

	for (int overlap = 1; overlap < k; overlap++) {
		unordered_map<string, vector<int>> lenPrefixes;
		for (auto& piece : noInPieces) {
			lenPrefixes[cover[piece].substr(0, overlap)].push_back(piece);
		}
		for (auto& outPiece : noOutPieces) {
			string kSuffix = cover[outPiece].substr(L - overlap);
			auto foundMatch = lenPrefixes.find(kSuffix);
			if (foundMatch != lenPrefixes.end()) {
				for (auto& inPiece : foundMatch->second) {
					if (outPiece == inPiece)
						continue;
					Edge edge(outPiece, inPiece, overlap);
					edgesByPiece[outPiece].out.push_back(edge);
					edgesByPiece[inPiece].in.push_back(edge);
				}
			}
		}
	}

	for (int overlap = k; overlap < TH; overlap++) {
		int position = L - overlap;
		for (auto& noOutPiece : noOutPieces) {
			auto foundKMatch = lenKPrefixes.find(cover[noOutPiece].substr(position, k));
			if (foundKMatch != lenKPrefixes.end()) {
				int len = L - position;
				for (auto& prefixPiece : foundKMatch->second) {
					if (noOutPiece == prefixPiece)
						continue;
					if (SuffixAIsPrefixB(cover[noOutPiece], cover[prefixPiece], L, len, k)) {
						Edge edge(noOutPiece, prefixPiece, len);
						edgesByPiece[noOutPiece].out.push_back(edge);
						edgesByPiece[prefixPiece].in.push_back(edge);
					}
				}
			}
		}
	}
	// if a piece has out edge with overlap>=TL delete out edges with overlap<TL. delete also corresponding in edges
	for (auto& noOutPiece : noOutPieces) {
		if (not edgesByPiece[noOutPiece].out.empty()) {
			Edge& longestEdge = edgesByPiece[noOutPiece].out.back();
			if (longestEdge.subpieceLen >= TL) {
				// delete out edges with overlap<TL
				for (vector<Edge>::iterator it = edgesByPiece[noOutPiece].out.begin(); it->subpieceLen < TL;) {
					edgesByPiece[it->to].DeleteInEdge(it->from, it->subpieceLen);
					it = edgesByPiece[noOutPiece].out.erase(it);
				}
			}
		}
	}
}

//void BelowTHEdgesByPieceMyHash(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
//		const int TL, const int k, const vector<int>& noOutPieces, const HashMap<vector<int> >& lenKPrefixes) {
//
//	vector<int> noInPieces;
//	for (vector<HashEntry<vector<int> > >::const_iterator entryIt = lenKPrefixes.entries.begin();
//			entryIt != lenKPrefixes.entries.end(); entryIt++) {
//		if (not entryIt->key.empty())
//			noInPieces.insert(noInPieces.end(), entryIt->value.begin(), entryIt->value.end());
//	}
//
//	for (int overlap = 1; overlap < k; overlap++) {
//		unordered_map<string, vector<int>> lenPrefixes;
//		for (auto& piece : noInPieces) {
//			lenPrefixes[cover[piece].substr(0, overlap)].push_back(piece);
//		}
//		for (auto& outPiece : noOutPieces) {
//			string kSuffix = cover[outPiece].substr(L - overlap);
//			auto foundMatch = lenPrefixes.find(kSuffix);
//			if (foundMatch != lenPrefixes.end()) {
//				for (auto& inPiece : foundMatch->second) {
//					if (outPiece == inPiece)
//						continue;
//					Edge edge(outPiece, inPiece, overlap);
//					edgesByPiece[outPiece].out.push_back(edge);
//					edgesByPiece[inPiece].in.push_back(edge);
//				}
//			}
//		}
//	}
//
//	for (int overlap = k; overlap < TH; overlap++) {
//		int position = L - overlap;
//		for (auto& noOutPiece : noOutPieces) {
//			vector<int> prefixVector;
//			bool foundKMatch = lenKPrefixes.Get(cover[noOutPiece].substr(position, k), prefixVector);
//			if (foundKMatch) {
//				int len = L - position;
//				for (auto& prefixPiece : prefixVector) {
//					if (noOutPiece == prefixPiece)
//						continue;
//					if (SuffixAIsPrefixB(cover[noOutPiece], cover[prefixPiece], L, len, k)) {
//						Edge edge(noOutPiece, prefixPiece, len);
//						edgesByPiece[noOutPiece].out.push_back(edge);
//						edgesByPiece[prefixPiece].in.push_back(edge);
//					}
//				}
//			}
//		}
//	}
//	// if a piece has out edge with overlap>=TL delete out edges with overlap<TL. delete also corresponding in edges
//	for (auto& noOutPiece : noOutPieces) {
//		if (not edgesByPiece[noOutPiece].out.empty()) {
//			Edge& longestEdge = edgesByPiece[noOutPiece].out.back();
//			if (longestEdge.subpieceLen >= TL) {
//				// delete out edges with overlap<TL
//				for (vector<Edge>::iterator it = edgesByPiece[noOutPiece].out.begin(); it->subpieceLen < TL;) {
//					edgesByPiece[it->to].DeleteInEdge(it->from, it->subpieceLen);
//					it = edgesByPiece[noOutPiece].out.erase(it);
//				}
//			}
//		}
//	}
//}

//void BelowTHEdgesByPieceCustomHash(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L,
//		const int TH, const int TL, const int k, const vector<int>& noOutPieces,
//		const unordered_map<string, vector<int>, GTACHasher>& lenKPrefixes) {
//
//	vector<int> noInPieces;
//	for (auto& pr : lenKPrefixes) {
//		noInPieces.insert(noInPieces.end(), pr.second.begin(), pr.second.end());
//	}
//
//	for (int overlap = 1; overlap < k; overlap++) {
//		unordered_map<string, vector<int>> lenPrefixes;
//		for (auto& piece : noInPieces) {
//			lenPrefixes[cover[piece].substr(0, overlap)].push_back(piece);
//		}
//		for (auto& outPiece : noOutPieces) {
//			string kSuffix = cover[outPiece].substr(L - overlap);
//			auto foundMatch = lenPrefixes.find(kSuffix);
//			if (foundMatch != lenPrefixes.end()) {
//				for (auto& inPiece : foundMatch->second) {
//					if (outPiece == inPiece)
//						continue;
//					Edge edge(outPiece, inPiece, overlap);
//					edgesByPiece[outPiece].out.push_back(edge);
//					edgesByPiece[inPiece].in.push_back(edge);
//				}
//			}
//		}
//	}
//
//	for (int overlap = k; overlap < TH; overlap++) {
//		int position = L - overlap;
//		for (auto& noOutPiece : noOutPieces) {
//			auto foundKMatch = lenKPrefixes.find(cover[noOutPiece].substr(position, k));
//			if (foundKMatch != lenKPrefixes.end()) {
//				int len = L - position;
//				for (auto& prefixPiece : foundKMatch->second) {
//					if (noOutPiece == prefixPiece)
//						continue;
//					if (SuffixAIsPrefixB(cover[noOutPiece], cover[prefixPiece], L, len, k)) {
//						Edge edge(noOutPiece, prefixPiece, len);
//						edgesByPiece[noOutPiece].out.push_back(edge);
//						edgesByPiece[prefixPiece].in.push_back(edge);
//					}
//				}
//			}
//		}
//	}
//	// if a piece has out edge with overlap>=TL delete out edges with overlap<TL. delete also corresponding in edges
//	for (auto& noOutPiece : noOutPieces) {
//		if (not edgesByPiece[noOutPiece].out.empty()) {
//			Edge& longestEdge = edgesByPiece[noOutPiece].out.back();
//			if (longestEdge.subpieceLen >= TL) {
//				// delete out edges with overlap<TL
//				for (vector<Edge>::iterator it = edgesByPiece[noOutPiece].out.begin(); it->subpieceLen < TL;) {
//					edgesByPiece[it->to].DeleteInEdge(it->from, it->subpieceLen);
//					it = edgesByPiece[noOutPiece].out.erase(it);
//				}
//			}
//		}
//	}
//}

// longest overlap edges for overlap >=TH
// 1 first all k len at position 1 to get L-1 connections. discard all pieces which were connected and continue to position 2,3,...
// 	 while connection >=TH
// 2 below TH: normal for all remaining vertices
// 3 for all (u,j) of step 1:	if overlap is repeated string (check O(len string)),
//								get all overlaps (no need to check, can be done by the repeated string
// set hashtable bucket num

void EdgesByPieceFast(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
		const int TL, const int k) {
	assert(TH < L and k < TH and k > 3);
	int coverSize = cover.size();
	edgesByPiece = vector<PieceEdges>(coverSize);
	unordered_map<string, vector<int>> lenKPrefixes; // (len k prefix, vector of pieces)
	vector<int> noOutPieces;
	vector<Edge> atLeastTHOutEdges;
	THEdgesByPiece(edgesByPiece, cover, L, TH, k, noOutPieces, lenKPrefixes, atLeastTHOutEdges);

	int repeatedSize;
	string overlap;
	// repeated string overlap case for longest overlap >= TH
	for (auto& edge : atLeastTHOutEdges) {
		overlap = cover[edge.to].substr(0, edge.subpieceLen);
		if (IsRepeated(overlap, repeatedSize)) {
			Edge newEdge = edge;
			for (int subpieceLen = edge.subpieceLen - repeatedSize; subpieceLen >= edge.subpieceLen / 2; subpieceLen -=
					repeatedSize) {
				newEdge.subpieceLen = subpieceLen;
				edgesByPiece[newEdge.from].out.insert(edgesByPiece[newEdge.from].out.begin(), newEdge);
				edgesByPiece[newEdge.to].in.insert(edgesByPiece[newEdge.to].in.begin(), newEdge);
			}
		}
	}

	BelowTHEdgesByPiece(edgesByPiece, cover, L, TH, TL, k, noOutPieces, lenKPrefixes);
}

struct Node {
	int prev;
	int next;
	Node() :
			prev(NA), next(NA) {

	}
};

struct SuffPrefMatch {
	const vector<string>& reads;
	int N;
	int L;
	int p;
	int T;
	unordered_map<char, int> charToNum;
	int fourInv;
	vector<int> fourPow;
	vector<int> lastPrefHash;
	int firstUnmatchedPref;
	vector<Node> unmatchedPref;
	vector<int> lastSuffHash;
	int firstUnmatchedSuff;
	vector<Node> unmatchedSuff;
	vector<vector<int> > hashTable;

	SuffPrefMatch(const vector<string>& cover, const int L, const int TH) :
			reads(cover), N(cover.size()), L(L), T(TH), fourPow(L - 1), lastPrefHash(N), unmatchedPref(N), lastSuffHash(
					N), unmatchedSuff(N) {
		p = FindNextPrime(N);
		charToNum = { {'A', 0}, {'C', 1}, {'G', 2}, {'T', 3}};
		fourInv = FourInv(p);
		fourPow[0] = 1;
		for (int i = 1; i <= L - 2; i++) {
			fourPow[i] = (fourPow[i - 1] * 4) % p;
		}
		firstUnmatchedPref = 0;
		firstUnmatchedSuff = 0;
		hashTable = vector<vector<int> >(p);
		InitPrevNext(unmatchedPref);
		InitPrevNext(unmatchedSuff);
	}

	bool UnmatchedEmpty() const {
		return (firstUnmatchedPref == NA) or (firstUnmatchedSuff == NA);
	}

	void InitPrevNext(vector<Node>& unmatched) {
		unmatched[0].prev = NA;
		unmatched[0].next = 1;

		for (int piece = 1; piece < N - 1; piece++) {
			unmatched[piece].prev = piece - 1;
			unmatched[piece].next = piece + 1;
		}

		unmatched[N - 1].prev = N - 2;
		unmatched[N - 1].next = NA;
	}

	// hash of the hashedLen length substring starting at MSLPos
	int FullHash(const string& str, const int MSLPos, const int hashedLen) {
		assert((MSLPos < (int )str.length()) and (MSLPos >= 0));
		assert((hashedLen > 0) and (hashedLen <= (int ) str.length()));
		assert(MSLPos + hashedLen <= (int )str.length());

		int hash = 0;
		for (int strIndex = MSLPos; strIndex < MSLPos + hashedLen; strIndex++) {
			hash = ((hash * 4) % p + charToNum[str[strIndex]]) % p;
		}
		assert((hash >= 0) and (hash < p));
		return hash;
	}

	// hash of the hashedLen length substring starting at MSLPos by prevHash
	// prevHash: hash of the hashedLen length substring starting at MSLPos-1
	int ShiftRightHash(const string& str, const int MSLPos, const int hashedLen, const int prevHash) {
		assert((MSLPos < (int )str.length()) and (MSLPos > 0));
		assert((hashedLen > 0) and (hashedLen <= (int ) str.length()));
		assert(MSLPos + hashedLen <= (int )str.length());
		assert(hashedLen <= (int ) fourPow.size());

		char previousMSL = str[MSLPos - 1];
		char currentLSL = str[MSLPos + hashedLen - 1];
		int hash = prevHash - (charToNum[previousMSL] * fourPow[hashedLen - 1]) % p;
		hash = hash < 0 ? hash + p : hash;
		hash = ((hash * 4) % p + charToNum[currentLSL]) % p;
		assert((hash >= 0) and (hash < p));
		return hash;
	}

	// hash of the hashedLen length substring starting at MSLPos by prevHash
	// prevHash: hash of the hashedLen+1 length substring starting at MSLPos-1
	int DiscardedMSLHash(const string& str, const int MSLPos, const int hashedLen, const int prevHash) {
		assert((MSLPos < (int )str.length()) and (MSLPos > 0));
		assert((hashedLen > 0) and (hashedLen < (int ) str.length()));
		assert(hashedLen <= (int ) fourPow.size());

		char previousMSL = str[MSLPos - 1];
		int hash = prevHash - (charToNum[previousMSL] * fourPow[hashedLen]) % p;
		hash = hash < 0 ? hash + p : hash;
		assert((hash >= 0) and (hash < p));
		return hash;
	}

	// hash of the hashedLen length substring starting at MSLPos by prevHash
	// prevHash: hash of the hashedLen+1 length substring starting at MSLPos
	int DiscardedLSLHash(const string& str, const int MSLPos, const int hashedLen, const int prevHash) {
		assert((MSLPos < (int )str.length()) and (MSLPos >= 0));
		assert((hashedLen > 0) and (hashedLen < (int ) str.length()));
		assert(MSLPos + hashedLen < (int )str.length());

		char previousLSL = str[MSLPos + hashedLen];
		long long longHash = prevHash - charToNum[previousLSL];
		longHash = longHash < 0 ? longHash + p : longHash;
		longHash = (longHash * fourInv) % p;
		int hash = longHash;
		assert((hash >= 0) and (hash < p));
		return hash;
	}

	int LMinusOnePrefHash(const string& prefix) {
		assert((int )prefix.size() == L - 1);
		assert(L > 2);
		int hash = (charToNum[prefix[0]] * fourPow[L - 2] + charToNum[prefix[1]] * fourPow[L - 3]) % p;
		for (int prefIndex = 2; prefIndex < L - 1; prefIndex++) {
			hash = (hash + charToNum[prefix[prefIndex]] * fourPow[L - 2 - prefIndex]) % p;
		}
		return hash;
	}

	// computation of L-1 prefixes hash
//	void LMinusOnePrefHashes() {
//		for (int piece = 0; piece < N; piece++) {
//			string prefix = reads[piece].substr(0, L - 1);
//			int hash = LMinusOnePrefHash(prefix);
//			lastPrefHash[piece] = hash;
//			hashTable[hash].push_back(piece);
//		}
//	}

	void LMinusOnePrefHashes() {
		for (int piece = 0; piece < N; piece++) {
			int hash = FullHash(reads[piece], 0, L - 1);
			lastPrefHash[piece] = hash;
			hashTable[hash].push_back(piece);
		}
	}

	// computation of L-1 suffixes hash by the L-1 prefixes hash
//	void LMinusOneSuffHashes() {
//		for (int piece = 0; piece < N; piece++) {
//			int lMinus1PrefHash = lastPrefHash[piece];
//			char firstLetter = reads[piece][0];
//			char lastLetter = reads[piece][L - 1];
//			int hash = lMinus1PrefHash - (charToNum[firstLetter] * fourPow[L - 2]) % p;
//			hash = hash < 0 ? hash + p : hash;
//			hash = ((hash * 4) % p + charToNum[lastLetter]) % p;
//			lastSuffHash[piece] = hash;
//		}
//	}

	void LMinusOneSuffHashes() {
		for (int piece = 0; piece < N; piece++) {
			int hash = ShiftRightHash(reads[piece], 1, L - 1, lastPrefHash[piece]);
			lastSuffHash[piece] = hash;
		}
	}

//	void NextPrefHashes(const int matchLen) {
//		hashTable = vector<vector<int> >(p);
//		for (int prefPiece = firstUnmatchedPref; prefPiece != NA; prefPiece = unmatchedPref[prefPiece].next) {
//			char lastLeastSignificantLetter = reads[prefPiece][matchLen];
//			assert(lastPrefHash[prefPiece] != NA);
//			long long longHash = lastPrefHash[prefPiece] - charToNum[lastLeastSignificantLetter];
//			longHash = longHash < 0 ? longHash + p : longHash;
//			longHash = (longHash * fourInv) % p;
//			int hash = longHash;
//			lastPrefHash[prefPiece] = hash;
//			assert((hash >= 0) and (hash < p));
//			hashTable[hash].push_back(prefPiece);
//		}
//	}

	void NextPrefHashes(const int matchLen) {
		hashTable = vector<vector<int> >(p);
		for (int piece = firstUnmatchedPref; piece != NA; piece = unmatchedPref[piece].next) {
			assert(lastPrefHash[piece] != NA);
			int hash = DiscardedLSLHash(reads[piece], 0, matchLen, lastPrefHash[piece]);
			lastPrefHash[piece] = hash;
			hashTable[hash].push_back(piece);
		}
	}

//	void NextSuffHashes(const int matchLen) {
//		for (int suffPiece = firstUnmatchedSuff; suffPiece != NA; suffPiece = unmatchedSuff[suffPiece].next) {
//			char lastMostSignificantLetter = reads[suffPiece][L - 1 - matchLen];
//			assert(lastSuffHash[suffPiece] != NA);
//			int hash = lastSuffHash[suffPiece] - (charToNum[lastMostSignificantLetter] * fourPow[matchLen]) % p;
//			hash = hash < 0 ? hash + p : hash;
//			lastSuffHash[suffPiece] = hash;
//		}
//	}

	void NextSuffHashes(const int matchLen) {
		for (int piece = firstUnmatchedSuff; piece != NA; piece = unmatchedSuff[piece].next) {
			assert(lastSuffHash[piece] != NA);
			int hash = DiscardedMSLHash(reads[piece], L - matchLen, matchLen, lastSuffHash[piece]);
			lastSuffHash[piece] = hash;
		}
	}

	void FindAtLeastTEdges(vector<PieceEdges>& edgesByPiece, const int matchLen) {
		for (int suffPiece = firstUnmatchedSuff; suffPiece != NA;) {
			int hash = lastSuffHash[suffPiece];
			int nextUnmatched = unmatchedSuff[suffPiece].next; // save next prior to possible delete
			for (vector<int>::iterator prefMatchIt = hashTable[hash].begin(); prefMatchIt != hashTable[hash].end();
					prefMatchIt++) {
				if (suffPiece == *prefMatchIt) // avoid self edges
					continue;
				if (SuffixAIsPrefixB(reads[suffPiece], reads[*prefMatchIt], L, matchLen)) {
					assert(matchLen >= T);
					int mLen;
					Edge edge(suffPiece, *prefMatchIt, matchLen);
					edgesByPiece[suffPiece].out.push_back(edge);
					edgesByPiece[*prefMatchIt].in.push_back(edge);
					if (PrefixIsAlmostRepeated(reads[*prefMatchIt], matchLen, mLen)) { // compute multi-edges
						if (mLen < T / 2) { // add multi-edges with weight > TH/2
							for (int weight = matchLen - mLen; weight > T / 2; weight -= mLen) {
								Edge edge(suffPiece, *prefMatchIt, weight);
								edgesByPiece[suffPiece].out.insert(edgesByPiece[suffPiece].out.begin(), edge);
								edgesByPiece[*prefMatchIt].in.insert(edgesByPiece[*prefMatchIt].in.begin(), edge);
							}
						}
					}

					// delete and update
					DeleteNode(suffPiece, unmatchedSuff, lastSuffHash, firstUnmatchedSuff);
					DeleteNode(*prefMatchIt, unmatchedPref, lastPrefHash, firstUnmatchedPref);
					DeleteFromTable(hash, prefMatchIt);
					break;
				}
			}
			suffPiece = nextUnmatched;
		}
	}

	void FindLessThanTEdges(vector<PieceEdges>& edgesByPiece, const int matchLen) {
		for (int suffPiece = firstUnmatchedSuff; suffPiece != NA; suffPiece = unmatchedSuff[suffPiece].next) {
			int hash = lastSuffHash[suffPiece];
			for (vector<int>::iterator prefMatchIt = hashTable[hash].begin(); prefMatchIt != hashTable[hash].end();
					prefMatchIt++) {
				if (suffPiece == *prefMatchIt) // avoid self edges
					continue;
				if (SuffixAIsPrefixB(reads[suffPiece], reads[*prefMatchIt], L, matchLen)) {
					assert(matchLen < T);
					Edge edge(suffPiece, *prefMatchIt, matchLen);
					edgesByPiece[suffPiece].out.push_back(edge);
					edgesByPiece[*prefMatchIt].in.push_back(edge);
				}
			}
		}
	}

	void DeleteFromTable(const int hash, vector<int>::iterator it) {
		hashTable[hash].erase(it);
	}

	void DeleteNode(const int index, vector<Node>& unmatched, vector<int>& lastHash, int& first) {
		assert((index >= 0) and (index < N));
		lastHash[index] = NA;

		// only item in the list
		if (unmatched[index].prev == NA and unmatched[index].next == NA) {
			first = NA;
			unmatched[index].prev = NA;
			unmatched[index].next = NA;
			return;
		}

		// item is first in list
		if (unmatched[index].prev == NA) { // next[index]!=NA
			first = unmatched[index].next;
			unmatched[unmatched[index].next].prev = NA;
			unmatched[index].prev = NA;
			unmatched[index].next = NA;
			return;
		}

		// item is last in list;
		if (unmatched[index].next == NA) { // prev[index]!=NA
			unmatched[unmatched[index].prev].next = NA;
			unmatched[index].prev = NA;
			unmatched[index].next = NA;
			return;
		}

		// item is in middle of list
		unmatched[unmatched[index].next].prev = unmatched[index].prev;
		unmatched[unmatched[index].prev].next = unmatched[index].next;
		unmatched[index].prev = NA;
		unmatched[index].next = NA;
	}
}
;

// edges sorted in ascending weight order

void EdgesByPieceFinal(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
		const int TL, const int k) {
	assert(not cover.empty());
	int N = cover.size();
	edgesByPiece = vector<PieceEdges>(N);
	SuffPrefMatch suffPrefMatch(cover, L, TH);
	suffPrefMatch.LMinusOnePrefHashes();
	suffPrefMatch.LMinusOneSuffHashes();
	suffPrefMatch.FindAtLeastTEdges(edgesByPiece, L - 1);
	if (suffPrefMatch.UnmatchedEmpty())
		return;
	for (int matchLen = L - 2; matchLen >= TH; matchLen--) {
		suffPrefMatch.NextPrefHashes(matchLen);
		suffPrefMatch.NextSuffHashes(matchLen);
		suffPrefMatch.FindAtLeastTEdges(edgesByPiece, matchLen);
		if (suffPrefMatch.UnmatchedEmpty())
			return;
	}
	for (int matchLen = TH - 1; matchLen > 0; matchLen--) {
		suffPrefMatch.NextPrefHashes(matchLen);
		suffPrefMatch.NextSuffHashes(matchLen);
		suffPrefMatch.FindLessThanTEdges(edgesByPiece, matchLen);
	}
}

struct SuffPrefMatchK {
	const vector<string>& reads;
	int N;
	int L;
	int p;
	int T;
	int K;
	unordered_map<char, int> charToNum;
	int fourInv;
	vector<int> fourPow;
	vector<int> lastPrefHash;
	int firstUnmatchedPref;
	vector<Node> unmatchedPref;
	vector<int> lastSuffHash;
	int firstUnmatchedSuff;
	vector<Node> unmatchedSuff;
	vector<vector<int> > hashTable;

	SuffPrefMatchK(const vector<string>& cover, const int L, const int TH) :
			reads(cover), N(cover.size()), L(L), T(TH), fourPow(L - 1), lastPrefHash(N), unmatchedPref(N), lastSuffHash(
					N), unmatchedSuff(N) {
		p = FindNextPrime(N);
		K = log(N) / log(4) + 4;
		assert(K < L);
		charToNum = { {'A', 0}, {'C', 1}, {'G', 2}, {'T', 3}};
		fourInv = FourInv(p);
		fourPow[0] = 1;
		for (int i = 1; i <= L - 2; i++) {
			fourPow[i] = (fourPow[i - 1] * 4) % p;
		}
		firstUnmatchedPref = 0;
		firstUnmatchedSuff = 0;
		hashTable = vector<vector<int> >(p);
		InitPrevNext(unmatchedPref);
		InitPrevNext(unmatchedSuff);
	}

	bool UnmatchedEmpty() const {
		return (firstUnmatchedPref == NA) or (firstUnmatchedSuff == NA);
	}

	void InitPrevNext(vector<Node>& unmatched) {
		unmatched[0].prev = NA;
		unmatched[0].next = 1;

		for (int piece = 1; piece < N - 1; piece++) {
			unmatched[piece].prev = piece - 1;
			unmatched[piece].next = piece + 1;
		}

		unmatched[N - 1].prev = N - 2;
		unmatched[N - 1].next = NA;
	}

	// hash of the hashedLen length substring starting at MSLPos
	int FullHash(const string& str, const int MSLPos, const int hashedLen) {
		assert((MSLPos < (int )str.length()) and (MSLPos >= 0));
		assert((hashedLen > 0) and (hashedLen <= (int ) str.length()));
		assert(MSLPos + hashedLen <= (int )str.length());

		int hash = 0;
		for (int strIndex = MSLPos; strIndex < MSLPos + hashedLen; strIndex++) {
			hash = ((hash * 4) % p + charToNum[str[strIndex]]) % p;
		}
		assert((hash >= 0) and (hash < p));
		return hash;
	}

	// hash of the hashedLen length substring starting at MSLPos by prevHash
	// prevHash: hash of the hashedLen length substring starting at MSLPos-1
	int ShiftRightHash(const string& str, const int MSLPos, const int hashedLen, const int prevHash) {
		assert((MSLPos < (int )str.length()) and (MSLPos > 0));
		assert((hashedLen > 0) and (hashedLen <= (int ) str.length()));
		assert(MSLPos + hashedLen <= (int )str.length());
		assert(hashedLen <= (int ) fourPow.size());

		char previousMSL = str[MSLPos - 1];
		char currentLSL = str[MSLPos + hashedLen - 1];
		int hash = prevHash - (charToNum[previousMSL] * fourPow[hashedLen - 1]) % p;
		hash = hash < 0 ? hash + p : hash;
		hash = ((hash * 4) % p + charToNum[currentLSL]) % p;
		assert((hash >= 0) and (hash < p));
		return hash;
	}

	// hash of the hashedLen length substring starting at MSLPos by prevHash
	// prevHash: hash of the hashedLen+1 length substring starting at MSLPos-1
	int DiscardedMSLHash(const string& str, const int MSLPos, const int hashedLen, const int prevHash) {
		assert((MSLPos < (int )str.length()) and (MSLPos > 0));
		assert((hashedLen > 0) and (hashedLen < (int ) str.length()));
		assert(hashedLen <= (int ) fourPow.size());

		char previousMSL = str[MSLPos - 1];
		int hash = prevHash - (charToNum[previousMSL] * fourPow[hashedLen]) % p;
		hash = hash < 0 ? hash + p : hash;
		assert((hash >= 0) and (hash < p));
		return hash;
	}

	// hash of the hashedLen length substring starting at MSLPos by prevHash
	// prevHash: hash of the hashedLen+1 length substring starting at MSLPos
	int DiscardedLSLHash(const string& str, const int MSLPos, const int hashedLen, const int prevHash) {
		assert((MSLPos < (int )str.length()) and (MSLPos >= 0));
		assert((hashedLen > 0) and (hashedLen < (int ) str.length()));
		assert(MSLPos + hashedLen < (int )str.length());

		char previousLSL = str[MSLPos + hashedLen];
		long long longHash = prevHash - charToNum[previousLSL];
		longHash = longHash < 0 ? longHash + p : longHash;
		longHash = (longHash * fourInv) % p;
		int hash = longHash;
		assert((hash >= 0) and (hash < p));
		return hash;
	}

	// hashes of first K letters of reads
	void KPrefHashes() {
		for (int piece = 0; piece < N; piece++) {
			int hash = FullHash(reads[piece], 0, K);
			lastPrefHash[piece] = hash;
			hashTable[hash].push_back(piece);
		}
	}

	// hashes of K letters starting at index 1
	void KSuffHashes() {
		for (int piece = 0; piece < N; piece++) {
			int hash = ShiftRightHash(reads[piece], 1, K, lastPrefHash[piece]);
			lastSuffHash[piece] = hash;
		}
	}

	void NextKSuffHashes(const int MSLPos) {
		for (int piece = firstUnmatchedSuff; piece != NA; piece = unmatchedSuff[piece].next) {
			assert(lastSuffHash[piece] != NA);
			int hash = ShiftRightHash(reads[piece], MSLPos, K, lastSuffHash[piece]);
			lastSuffHash[piece] = hash;
		}
	}

	void NextPrefHashes(const int matchLen) {
		hashTable = vector<vector<int> >(p);
		for (int piece = firstUnmatchedPref; piece != NA; piece = unmatchedPref[piece].next) {
			assert(lastPrefHash[piece] != NA);
			int hash = DiscardedLSLHash(reads[piece], 0, matchLen, lastPrefHash[piece]);
			lastPrefHash[piece] = hash;
			hashTable[hash].push_back(piece);
		}
	}

	void NextSuffHashes(const int matchLen) {
		for (int piece = firstUnmatchedSuff; piece != NA; piece = unmatchedSuff[piece].next) {
			assert(lastSuffHash[piece] != NA);
			int hash = DiscardedMSLHash(reads[piece], L - matchLen, matchLen, lastSuffHash[piece]);
			lastSuffHash[piece] = hash;
		}
	}

	void FindAtLeastTEdges(vector<PieceEdges>& edgesByPiece, const int matchLen) {
		for (int suffPiece = firstUnmatchedSuff; suffPiece != NA;) {
			int hash = lastSuffHash[suffPiece];
			int nextUnmatched = unmatchedSuff[suffPiece].next; // save next prior to possible delete
			for (vector<int>::iterator prefMatchIt = hashTable[hash].begin(); prefMatchIt != hashTable[hash].end();
					prefMatchIt++) {
				if (suffPiece == *prefMatchIt) // avoid self edges
					continue;
				if (SuffixAIsPrefixB(reads[suffPiece], reads[*prefMatchIt], L, matchLen)) {
					assert(matchLen >= T);
					int mLen;
					Edge edge(suffPiece, *prefMatchIt, matchLen);
					edgesByPiece[suffPiece].out.push_back(edge);
					edgesByPiece[*prefMatchIt].in.push_back(edge);
					if (PrefixIsAlmostRepeated(reads[*prefMatchIt], matchLen, mLen)) { // compute multi-edges
						if (mLen < T / 2) { // add multi-edges with weight > TH/2
							for (int weight = matchLen - mLen; weight > T / 2; weight -= mLen) {
								Edge edge(suffPiece, *prefMatchIt, weight);
								edgesByPiece[suffPiece].out.insert(edgesByPiece[suffPiece].out.begin(), edge);
								edgesByPiece[*prefMatchIt].in.insert(edgesByPiece[*prefMatchIt].in.begin(), edge);
							}
						}
					}

					// delete and update
					DeleteNode(suffPiece, unmatchedSuff, lastSuffHash, firstUnmatchedSuff);
					DeleteNode(*prefMatchIt, unmatchedPref, lastPrefHash, firstUnmatchedPref);
					DeleteFromTable(hash, prefMatchIt);
					break;
				}
			}
			suffPiece = nextUnmatched;
		}
	}

	void FindLessThanTEdges(vector<PieceEdges>& edgesByPiece, const int matchLen) {
		for (int suffPiece = firstUnmatchedSuff; suffPiece != NA; suffPiece = unmatchedSuff[suffPiece].next) {
			int hash = lastSuffHash[suffPiece];
			for (vector<int>::iterator prefMatchIt = hashTable[hash].begin(); prefMatchIt != hashTable[hash].end();
					prefMatchIt++) {
				if (suffPiece == *prefMatchIt) // avoid self edges
					continue;
				if (SuffixAIsPrefixB(reads[suffPiece], reads[*prefMatchIt], L, matchLen)) {
					assert(matchLen < T);
					Edge edge(suffPiece, *prefMatchIt, matchLen);
					edgesByPiece[suffPiece].out.push_back(edge);
					edgesByPiece[*prefMatchIt].in.push_back(edge);
				}
			}
		}
	}

	void DeleteFromTable(const int hash, vector<int>::iterator it) {
		hashTable[hash].erase(it);
	}

	void DeleteNode(const int index, vector<Node>& unmatched, vector<int>& lastHash, int& first) {
		assert((index >= 0) and (index < N));
		lastHash[index] = NA;

		// only item in the list
		if (unmatched[index].prev == NA and unmatched[index].next == NA) {
			first = NA;
			unmatched[index].prev = NA;
			unmatched[index].next = NA;
			return;
		}

		// item is first in list
		if (unmatched[index].prev == NA) { // next[index]!=NA
			first = unmatched[index].next;
			unmatched[unmatched[index].next].prev = NA;
			unmatched[index].prev = NA;
			unmatched[index].next = NA;
			return;
		}

		// item is last in list;
		if (unmatched[index].next == NA) { // prev[index]!=NA
			unmatched[unmatched[index].prev].next = NA;
			unmatched[index].prev = NA;
			unmatched[index].next = NA;
			return;
		}

		// item is in middle of list
		unmatched[unmatched[index].next].prev = unmatched[index].prev;
		unmatched[unmatched[index].prev].next = unmatched[index].next;
		unmatched[index].prev = NA;
		unmatched[index].next = NA;
	}
};

// dummyA, dummyB not used. just for compatibility with function pointer
void EdgesByPieceFinalK(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
		const int dummyA, const int dummyB) {
	assert(not cover.empty());
	int N = cover.size();
	edgesByPiece = vector<PieceEdges>(N);
	SuffPrefMatchK suffPrefMatch(cover, L, TH);
	int K = suffPrefMatch.K;
	if (K < TH) {
		suffPrefMatch.KPrefHashes();
		suffPrefMatch.KSuffHashes();
		suffPrefMatch.FindAtLeastTEdges(edgesByPiece, L - 1);
		if (suffPrefMatch.UnmatchedEmpty())
			return;
		for (int matchLen = L - 2; matchLen >= TH; matchLen--) {
			suffPrefMatch.NextKSuffHashes(L - matchLen);
			suffPrefMatch.FindAtLeastTEdges(edgesByPiece, matchLen);
			if (suffPrefMatch.UnmatchedEmpty())
				return;
		}
		for (int matchLen = TH - 1; matchLen >= K; matchLen--) {
			suffPrefMatch.NextKSuffHashes(L - matchLen);
			suffPrefMatch.FindLessThanTEdges(edgesByPiece, matchLen);
		}
		for (int matchLen = K - 1; matchLen > 0; matchLen--) {
			suffPrefMatch.NextPrefHashes(matchLen);
			suffPrefMatch.NextSuffHashes(matchLen);
			suffPrefMatch.FindLessThanTEdges(edgesByPiece, matchLen);
		}
	}
	else { // K>=TH
		suffPrefMatch.KPrefHashes();
		suffPrefMatch.KSuffHashes();
		suffPrefMatch.FindAtLeastTEdges(edgesByPiece, L - 1);
		if (suffPrefMatch.UnmatchedEmpty())
			return;
		for (int matchLen = L - 2; matchLen >= K; matchLen--) {
			suffPrefMatch.NextKSuffHashes(L - matchLen);
			suffPrefMatch.FindAtLeastTEdges(edgesByPiece, matchLen);
			if (suffPrefMatch.UnmatchedEmpty())
				return;
		}

		for (int matchLen = K - 1; matchLen >= TH; matchLen--) {
			suffPrefMatch.NextPrefHashes(matchLen);
			suffPrefMatch.NextSuffHashes(matchLen);
			suffPrefMatch.FindAtLeastTEdges(edgesByPiece, matchLen);
			if (suffPrefMatch.UnmatchedEmpty())
				return;
		}

		for (int matchLen = TH - 1; matchLen > 0; matchLen--) {
			suffPrefMatch.NextPrefHashes(matchLen);
			suffPrefMatch.NextSuffHashes(matchLen);
			suffPrefMatch.FindLessThanTEdges(edgesByPiece, matchLen);
		}
	}
}

//void EdgesByPieceFastMyHash(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L, const int TH,
//		const int TL, const int k) {
//	assert(TH < L and k < TH and k > 3);
//	int coverSize = cover.size();
//	edgesByPiece = vector<PieceEdges>(coverSize);
//	HashMap<vector<int> > lenKPrefixes; // (len k prefix, vector of pieces)
//	vector<int> noOutPieces;
//	vector<Edge> atLeastTHOutEdges;
//	THEdgesByPieceMyHash(edgesByPiece, cover, L, TH, k, noOutPieces, lenKPrefixes, atLeastTHOutEdges);
//
//	int repeatedSize;
//	string overlap;
//// repeated string overlap case for longest overlap >= TH
//	for (auto& edge : atLeastTHOutEdges) {
//		overlap = cover[edge.to].substr(0, edge.subpieceLen);
//		if (IsRepeated(overlap, repeatedSize)) {
//			Edge newEdge = edge;
//			for (int subpieceLen = edge.subpieceLen - repeatedSize; subpieceLen >= edge.subpieceLen / 2; subpieceLen -=
//					repeatedSize) {
//				newEdge.subpieceLen = subpieceLen;
//				edgesByPiece[newEdge.from].out.insert(edgesByPiece[newEdge.from].out.begin(), newEdge);
//				edgesByPiece[newEdge.to].in.insert(edgesByPiece[newEdge.to].in.begin(), newEdge);
//			}
//		}
//	}
//
//	BelowTHEdgesByPieceMyHash(edgesByPiece, cover, L, TH, TL, k, noOutPieces, lenKPrefixes);
//}

//void EdgesByPieceFastCustomHash(vector<PieceEdges>& edgesByPiece, const vector<string>& cover, const int L,
//		const int TH, const int TL, const int k) {
//	assert(TH < L and k < TH and k > 3);
//	int coverSize = cover.size();
//	edgesByPiece = vector<PieceEdges>(coverSize);
//	unordered_map<string, vector<int>, GTACHasher> lenKPrefixes; // (len k prefix, vector of pieces)
//	vector<int> noOutPieces;
//	vector<Edge> atLeastTHOutEdges;
//	THEdgesByPieceCustomHash(edgesByPiece, cover, L, TH, k, noOutPieces, lenKPrefixes, atLeastTHOutEdges);
//
//	int repeatedSize;
//	string overlap;
//// repeated string overlap case for longest overlap >= TH
//	for (auto& edge : atLeastTHOutEdges) {
//		overlap = cover[edge.to].substr(0, edge.subpieceLen);
//		if (IsRepeated(overlap, repeatedSize)) {
//			Edge newEdge = edge;
//			for (int subpieceLen = edge.subpieceLen - repeatedSize; subpieceLen >= edge.subpieceLen / 2; subpieceLen -=
//					repeatedSize) {
//				newEdge.subpieceLen = subpieceLen;
//				edgesByPiece[newEdge.from].out.insert(edgesByPiece[newEdge.from].out.begin(), newEdge);
//				edgesByPiece[newEdge.to].in.insert(edgesByPiece[newEdge.to].in.begin(), newEdge);
//			}
//		}
//	}
//
//	BelowTHEdgesByPieceCustomHash(edgesByPiece, cover, L, TH, TL, k, noOutPieces, lenKPrefixes);
//}

void PrintSubpieceHashTable(const unordered_map<string, SubpieceMatch>& subpieceHashTable) {
	for (auto& pr : subpieceHashTable) {
		if (pr.second.prefixOf.empty() or pr.second.suffixOf.empty())
			continue;
		cout << "subpiece:\t" << pr.first << endl;
		cout << "prefix of:\t";
		for (auto& prfOf : pr.second.prefixOf) {
			cout << prfOf << '\t';
		}
		cout << endl;
		cout << "suffix of:\t";
		for (auto& sfxOf : pr.second.suffixOf) {
			cout << sfxOf << '\t';
		}
		cout << endl;
		cout << "+++++++++++++++++++++++++++++++++++++" << endl;
	}
}

void PrintPieceTable(const vector<PieceEdges>& pieceTable) {
	for (unsigned i = 0; i < pieceTable.size(); i++) {
		cout << "piece:\t" << i << endl;
		cout << "In Edges:" << endl;
		for (auto& inEdge : pieceTable[i].in) {
			cout << inEdge.from << '\t' << inEdge.subpieceLen << endl;
		}
		cout << "Out Edges:" << endl;
		for (auto& outEdge : pieceTable[i].out) {
			cout << outEdge.to << '\t' << outEdge.subpieceLen << endl;
		}
		cout << "***********************************" << endl;
	}
}

void PrintCover(const vector<string>& cover) {
	cout << "Cover:" << endl;
	for (unsigned i = 0; i < cover.size(); i++) {
		cout << i << '\t' << cover[i] << endl;
	}
}
